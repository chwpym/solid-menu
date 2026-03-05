from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import (
    Mesa,
    Cliente,
    Fornecedor,
    Entregador,
    FormaPagamento,
    TaxaEntrega,
    Impressora,
    Configuracao,
)
from schemas import cadastros
from security import get_current_admin, get_current_caixa

router = APIRouter(prefix="/api/cadastros", tags=["Cadastros Auxiliares"])


def generic_crud(model, schema_create, schema_response, tag_name: str, path: str):
    """Factory helper para evitar repetição massiva de CRUDs simples."""
    sub_router = APIRouter(prefix=path, tags=[tag_name])

    @sub_router.get("/", response_model=List[schema_response])
    def listar(db: Session = Depends(get_db)):
        return db.query(model).all()

    @sub_router.post(
        "/", response_model=schema_response, dependencies=[Depends(get_current_admin)]
    )
    def criar(item: schema_create, db: Session = Depends(get_db)):
        db_item = model(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @sub_router.put(
        "/{item_id}",
        response_model=schema_response,
        dependencies=[Depends(get_current_admin)],
    )
    def atualizar(item_id: int, item: schema_create, db: Session = Depends(get_db)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail="Não encontrado")
        for k, v in item.model_dump().items():
            setattr(db_item, k, v)
        db.commit()
        db.refresh(db_item)
        return db_item

    @sub_router.delete("/{item_id}", dependencies=[Depends(get_current_admin)])
    def inativar(item_id: int, db: Session = Depends(get_db)):
        db_item = db.query(model).filter(model.id == item_id).first()
        if db_item and hasattr(db_item, "ativo"):
            db_item.ativo = False
            db.commit()
        return {"msg": "Removido/Inativado com sucesso"}

    return sub_router


# Registra todos os sub-routers gerados
router.include_router(
    generic_crud(Mesa, cadastros.MesaCreate, cadastros.MesaResponse, "Mesas", "/mesas")
)
router.include_router(
    generic_crud(
        Cliente,
        cadastros.ClienteCreate,
        cadastros.ClienteResponse,
        "Clientes",
        "/clientes",
    )
)
router.include_router(
    generic_crud(
        Fornecedor,
        cadastros.FornecedorCreate,
        cadastros.FornecedorResponse,
        "Fornecedores",
        "/fornecedores",
    )
)
router.include_router(
    generic_crud(
        Entregador,
        cadastros.EntregadorCreate,
        cadastros.EntregadorResponse,
        "Entregadores",
        "/entregadores",
    )
)
router.include_router(
    generic_crud(
        FormaPagamento,
        cadastros.FormaPagamentoCreate,
        cadastros.FormaPagamentoResponse,
        "Formas Pagamento",
        "/formas-pagamento",
    )
)
router.include_router(
    generic_crud(
        TaxaEntrega,
        cadastros.TaxaEntregaCreate,
        cadastros.TaxaEntregaResponse,
        "Taxas Entrega",
        "/taxas-entrega",
    )
)
router.include_router(
    generic_crud(
        Impressora,
        cadastros.ImpressoraCreate,
        cadastros.ImpressoraResponse,
        "Impressoras",
        "/impressoras",
    )
)


# Configuração é um pouco diferente, permite atualizações direto pelo caixa/admin
@router.get("/configuracoes", response_model=List[cadastros.ConfiguracaoResponse])
def listar_config(db: Session = Depends(get_db)):
    return db.query(Configuracao).all()


@router.put(
    "/configuracoes/{chave}",
    response_model=cadastros.ConfiguracaoResponse,
    dependencies=[Depends(get_current_admin)],
)
def atualizar_config(
    chave: str, item: cadastros.ConfiguracaoCreate, db: Session = Depends(get_db)
):
    db_item = db.query(Configuracao).filter(Configuracao.chave == chave).first()
    if not db_item:
        db_item = Configuracao(chave=chave)
        db.add(db_item)

    for k, v in item.model_dump().items():
        if k != "chave":  # chave é inalterável via put no mesmo endpoint
            setattr(db_item, k, v)

    db.commit()
    db.refresh(db_item)
    return db_item
