from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import (
    Pedido,
    ItemPedido,
    ItemAdicional,
    DeliveryInfo,
    PedidoPagamento,
    Mesa,
    AuditLog,
)
from schemas import pedido as schemas
from security import get_current_user, get_current_caixa
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/pedidos", tags=["Pedidos"])


@router.post("/", response_model=schemas.PedidoResponse)
def criar_pedido(
    dados: schemas.PedidoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Cria um novo pedido (Mesa, Delivery ou Balcão) com seus itens e info de entrega."""

    # 1. Validações básicas de negócio
    if dados.tipo == "mesa" and not dados.mesa_id:
        raise HTTPException(status_code=400, detail="Pedido de mesa exige mesa_id")
    if dados.tipo == "delivery" and not dados.delivery_info:
        raise HTTPException(status_code=400, detail="Delivery exige delivery_info")

    # 2. Verifica e ocupa a mesa se for o caso
    if dados.tipo == "mesa":
        mesa = db.query(Mesa).filter(Mesa.id == dados.mesa_id).first()
        if not mesa:
            raise HTTPException(status_code=404, detail="Mesa não encontrada")
        if mesa.status != "Livre":
            raise HTTPException(
                status_code=400, detail="Mesa já ocupada ou indisponível"
            )
        mesa.status = "Ocupada"

    # 3. Calcula o valor total provisório e cria Pedido
    total = sum(
        [
            (i.preco_unitario * i.quantidade)
            + sum([a.preco_unitario * a.quantidade for a in i.adicionais])
            for i in dados.itens
        ]
    )

    db_pedido = Pedido(
        tipo=dados.tipo,
        status="novo",
        cliente_id=dados.cliente_id,
        mesa_id=dados.mesa_id,
        usuario_id=current_user.id,
        valor_total=total,
        observacao=dados.observacao,
    )
    db.add(db_pedido)
    db.flush()  # Para ganhar o ID

    # 4. Associa os itens e adicionais
    for idx_item, item in enumerate(dados.itens):
        db_item = ItemPedido(
            pedido_id=db_pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario,
            observacao=item.observacao,
            borda_id=item.borda_id,
            status="novo",
        )
        db.add(db_item)
        db.flush()

        for adc in item.adicionais:
            db_adc = ItemAdicional(
                item_id=db_item.id,
                adicional_id=adc.adicional_id,
                quantidade=adc.quantidade,
                preco_unitario=adc.preco_unitario,
            )
            db.add(db_adc)

    # 5. Delivery info
    if dados.tipo == "delivery" and dados.delivery_info:
        info = DeliveryInfo(**dados.delivery_info.model_dump(), pedido_id=db_pedido.id)
        db.add(info)

    db.commit()
    db.refresh(db_pedido)

    # IMPORTANTE: A integração com WEBSOCKET virá aqui na Fase 3 para notificar a Cozinha

    return db_pedido


@router.get("/", response_model=List[schemas.PedidoResponse])
def listar_pedidos_abertos(db: Session = Depends(get_db)):
    """Lista todos os pedidos que não estão fechados ou cancelados."""
    return db.query(Pedido).filter(~Pedido.status.in_(["cancelado", "fechado"])).all()


@router.get("/{pedido_id}", response_model=schemas.PedidoResponse)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.put(
    "/{pedido_id}/fechar",
    response_model=schemas.PedidoResponse,
    dependencies=[Depends(get_current_caixa)],
)
def fechar_pedido(
    pedido_id: int,
    fechamento: schemas.PedidoFechamento,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_caixa),
):
    """Fecha o pedido, processa pagamentos mistos ou marca como fiado."""
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.status == "fechado":
        raise HTTPException(status_code=400, detail="Pedido já fechado")

    # 1. Validação de pagamentos cobrindo o total (se não for fiado)
    if fechamento.forma_fechamento == "pago":
        total_pago = sum([p.valor for p in fechamento.pagamentos])
        # Logica basica: total_pago deve ser >= (valor_total - desconto)
        valor_devido = pedido.valor_total - fechamento.desconto
        if total_pago < valor_devido:
            raise HTTPException(
                status_code=400,
                detail=f"Valor pago ({total_pago}) é menor que o devido ({valor_devido})",
            )

        # Registra pagamentos na tabela N para 1
        for pgto in fechamento.pagamentos:
            db_pgto = PedidoPagamento(**pgto.model_dump(), pedido_id=pedido.id)
            db.add(db_pgto)

    # 2. Fiado exige cliente
    elif fechamento.forma_fechamento == "fiado":
        if not pedido.cliente_id:
            raise HTTPException(
                status_code=400, detail="Pedidos 'Fiado' exigem um Cliente vinculado."
            )
    else:
        raise HTTPException(status_code=400, detail="Forma de fechamento inválida.")

    # 3. Libera a mesa se era pedido local
    if pedido.tipo == "mesa" and pedido.mesa_id:
        mesa = db.query(Mesa).filter(Mesa.id == pedido.mesa_id).first()
        if mesa:
            mesa.status = "Livre"

    # Audit log para descontos
    if fechamento.desconto > 0:
        log = AuditLog(
            usuario_id=current_user.id,
            acao="APLICAR_DESCONTO",
            tabela="pedidos",
            registro_id=str(pedido.id),
            detalhe=f"Desconto de R${fechamento.desconto}",
            dados={
                "desconto": float(fechamento.desconto),
                "total_original": float(pedido.valor_total),
            },
        )
        db.add(log)

    # 4. Finaliza
    pedido.status = "fechado"
    pedido.desconto = fechamento.desconto
    pedido.forma_fechamento = fechamento.forma_fechamento

    db.commit()
    db.refresh(pedido)
    return pedido


@router.delete("/{pedido_id}", dependencies=[Depends(get_current_caixa)])
def cancelar_pedido(
    pedido_id: int,
    motivo: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_caixa),
):
    """Cancela o pedido. Ação logada na auditoria."""
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Não encontrado")

    if pedido.status == "fechado":
        raise HTTPException(
            status_code=400,
            detail="Não pode cancelar pedido fechado. Estorne primeiro.",
        )

    # Libera mesa
    if pedido.tipo == "mesa" and pedido.mesa_id:
        mesa = db.query(Mesa).filter(Mesa.id == pedido.mesa_id).first()
        if mesa:
            mesa.status = "Livre"

    # Audit log de cancelamento
    log = AuditLog(
        usuario_id=current_user.id,
        acao="CANCELAR_PEDIDO",
        tabela="pedidos",
        registro_id=str(pedido.id),
        detalhe=f"Motivo: {motivo}",
        dados={"total": float(pedido.valor_total), "tipo": pedido.tipo},
    )
    db.add(log)

    pedido.status = "cancelado"
    db.commit()

    return {"msg": "Pedido cancelado com sucesso."}


@router.patch("/{pedido_id}/status")
def atualizar_status(pedido_id: int, novo_status: str, db: Session = Depends(get_db)):
    """Fluxo do Kanban/KDS: novo -> preparando -> pronto -> enviado"""
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Não encontrado")

    pedido.status = novo_status
    db.commit()
    return {"msg": f"Status atualizado para {novo_status}"}
