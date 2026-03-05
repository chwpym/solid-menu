from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timezone

from database import get_db
from models import ContaPagar, Caixa, Sangria, PedidoPagamento, Pedido
from schemas import financeiro as schemas
from security import get_current_admin, get_current_caixa, get_current_user
from services.caixa import (
    require_nenhum_caixa_aberto,
    require_caixa_aberto,
    get_caixa_aberto,
)

router = APIRouter(prefix="/api/financeiro", tags=["Financeiro"])


# ==========================================
# CONTAS A PAGAR
# ==========================================
@router.get(
    "/contas-pagar",
    response_model=List[schemas.ContaPagarResponse],
    dependencies=[Depends(get_current_admin)],
)
def listar_contas(db: Session = Depends(get_db)):
    return db.query(ContaPagar).all()


@router.post(
    "/contas-pagar",
    response_model=schemas.ContaPagarResponse,
    dependencies=[Depends(get_current_admin)],
)
def criar_conta(item: schemas.ContaPagarCreate, db: Session = Depends(get_db)):
    db_item = ContaPagar(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put(
    "/contas-pagar/{item_id}",
    response_model=schemas.ContaPagarResponse,
    dependencies=[Depends(get_current_admin)],
)
def atualizar_conta(
    item_id: int, item: schemas.ContaPagarUpdate, db: Session = Depends(get_db)
):
    db_item = db.query(ContaPagar).filter(ContaPagar.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Não encontrado")
    for k, v in item.model_dump().items():
        setattr(db_item, k, v)
    db.commit()
    db.refresh(db_item)
    return db_item


# ==========================================
# CAIXA E SANGRIAS
# ==========================================
@router.get("/caixa/atual", response_model=schemas.CaixaResponse)
def obter_caixa_atual(
    db: Session = Depends(get_db), current_user=Depends(get_current_caixa)
):
    caixa = get_caixa_aberto(db)
    if not caixa:
        raise HTTPException(status_code=404, detail="Nenhum caixa aberto")
    return caixa


@router.post("/caixa/abrir", response_model=schemas.CaixaResponse)
def abrir_caixa(
    caixa_data: schemas.CaixaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_caixa),
):
    require_nenhum_caixa_aberto(db)
    novo_caixa = Caixa(
        fundo_inicial=caixa_data.fundo_inicial, usuario_id=current_user.id
    )
    db.add(novo_caixa)
    db.commit()
    db.refresh(novo_caixa)
    return novo_caixa


@router.post("/caixa/sangria", response_model=schemas.SangriaResponse)
def realizar_sangria(
    data: schemas.SangriaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_caixa),
):
    caixa_aberto = require_caixa_aberto(db)
    sangria = Sangria(
        caixa_id=caixa_aberto.id,
        usuario_id=current_user.id,
        valor=data.valor,
        motivo=data.motivo,
    )
    db.add(sangria)
    db.commit()
    db.refresh(sangria)
    return sangria


@router.post("/caixa/fechar", response_model=schemas.CaixaResponse)
def fechar_caixa(
    data: schemas.CaixaFechamento,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_caixa),
):
    caixa_aberto = require_caixa_aberto(db)

    # 1. Calcula os recebimentos do dia no período
    recebimentos = (
        db.query(func.sum(PedidoPagamento.valor))
        .join(Pedido)
        .filter(Pedido.data_hora >= caixa_aberto.data_abertura)
        .scalar()
        or 0
    )

    # 2. Calcula as retiradas (sangrias)
    sangrias = sum([s.valor for s in caixa_aberto.sangrias])

    # 3. Total Esperado = Fundo Inicial + Entradas - Saídas
    total_esperado = caixa_aberto.fundo_inicial + recebimentos - sangrias

    caixa_aberto.total_esperado = total_esperado
    caixa_aberto.total_contado = data.total_contado
    caixa_aberto.data_fechamento = datetime.now(timezone.utc)
    caixa_aberto.status = "Fechado"

    db.commit()
    db.refresh(caixa_aberto)
    return caixa_aberto
