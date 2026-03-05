from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Insumo, Receita, EntradaEstoque, Usuario
from schemas import estoque as schemas
from security import get_current_admin, get_current_caixa

router = APIRouter(prefix="/api/estoque", tags=["Estoque"])


# ==========================================
# INSUMOS
# ==========================================
@router.get("/insumos", response_model=List[schemas.InsumoResponse])
def listar_insumos(db: Session = Depends(get_db)):
    return db.query(Insumo).filter(Insumo.ativo == True).all()


@router.post(
    "/insumos",
    response_model=schemas.InsumoResponse,
    dependencies=[Depends(get_current_admin)],
)
def criar_insumo(item: schemas.InsumoCreate, db: Session = Depends(get_db)):
    db_item = Insumo(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put(
    "/insumos/{item_id}",
    response_model=schemas.InsumoResponse,
    dependencies=[Depends(get_current_admin)],
)
def atualizar_insumo(
    item_id: int, item: schemas.InsumoBase, db: Session = Depends(get_db)
):
    db_item = db.query(Insumo).filter(Insumo.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Não encontrado")

    # Observe que atualizar não altera estoque_atual (deve ser via EntradaEstoque)
    db_item.nome = item.nome
    db_item.unidade = item.unidade
    db_item.estoque_minimo = item.estoque_minimo
    db_item.ativo = item.ativo

    db.commit()
    db.refresh(db_item)
    return db_item


# ==========================================
# RECEITAS
# ==========================================
@router.get("/receitas", response_model=List[schemas.ReceitaResponse])
def listar_receitas(db: Session = Depends(get_db)):
    """Poderia ser filtrado por produto id, mas retorna tudo p/ simplificar"""
    return db.query(Receita).all()


@router.post(
    "/receitas",
    response_model=schemas.ReceitaResponse,
    dependencies=[Depends(get_current_admin)],
)
def criar_receita(item: schemas.ReceitaCreate, db: Session = Depends(get_db)):
    db_item = Receita(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/receitas/{item_id}", dependencies=[Depends(get_current_admin)])
def deletar_receita(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Receita).filter(Receita.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return {"msg": "Removido com sucesso"}


# ==========================================
# MOVIMENTAÇÕES MANUAIS
# ==========================================
@router.post("/entrada", response_model=schemas.EntradaEstoqueResponse)
def lancar_entrada_estoque(
    item: schemas.EntradaEstoqueCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_admin),
):
    """
    Registra entrada de estoque e soma a quantidade no Insumo atual.
    Usado quando não via NF-e XML.
    """
    insumo = db.query(Insumo).filter(Insumo.id == item.insumo_id).first()
    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo não encontrado")

    db_entrada = EntradaEstoque(**item.model_dump(), usuario_id=current_user.id)
    db.add(db_entrada)

    # Atualiza saldo do insumo
    insumo.estoque_atual += item.quantidade

    db.commit()
    db.refresh(db_entrada)
    return db_entrada
