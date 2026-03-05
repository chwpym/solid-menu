from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Categoria, Produto, Adicional, TipoBorda, LocalProducao
from schemas.cardapio import (
    CategoriaCreate,
    CategoriaResponse,
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse,
    AdicionalCreate,
    AdicionalResponse,
    TipoBordaCreate,
    TipoBordaResponse,
    LocalProducaoCreate,
    LocalProducaoResponse,
)
from security import get_current_admin, get_current_caixa

# Usaremos um único router aglutinador para o Cardápio
router = APIRouter(prefix="/api", tags=["Cardapio"])


# ==========================================
# CATEGORIAS
# ==========================================
@router.get("/categorias", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).order_by(Categoria.ordem).all()


@router.post(
    "/categorias",
    response_model=CategoriaResponse,
    dependencies=[Depends(get_current_admin)],
)
def criar_categoria(cat: CategoriaCreate, db: Session = Depends(get_db)):
    db_cat = Categoria(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.put(
    "/categorias/{cat_id}",
    response_model=CategoriaResponse,
    dependencies=[Depends(get_current_admin)],
)
def atualizar_categoria(
    cat_id: int, cat: CategoriaCreate, db: Session = Depends(get_db)
):
    db_cat = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Não encontrado")

    for key, value in cat.model_dump().items():
        setattr(db_cat, key, value)

    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.delete("/categorias/{cat_id}", dependencies=[Depends(get_current_admin)])
def remover_categoria(cat_id: int, db: Session = Depends(get_db)):
    db_cat = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Não encontrado")

    # Inativa ao invés de deletar para manter integridade
    db_cat.ativo = False
    db.commit()
    return {"msg": "Inativado com sucesso"}


# ==========================================
# PRODUTOS
# ==========================================
@router.get("/produtos", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()


@router.post(
    "/produtos",
    response_model=ProdutoResponse,
    dependencies=[Depends(get_current_admin)],
)
def criar_produto(prod: ProdutoCreate, db: Session = Depends(get_db)):
    # Remove lista de IDs do dicionário base
    prod_data = prod.model_dump(exclude={"adicionais_ids"})
    db_prod = Produto(**prod_data)

    # Vincula os adicionais, se houver
    if prod.adicionais_ids:
        adcs = db.query(Adicional).filter(Adicional.id.in_(prod.adicionais_ids)).all()
        db_prod.adicionais = adcs

    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod


@router.put(
    "/produtos/{prod_id}",
    response_model=ProdutoResponse,
    dependencies=[Depends(get_current_admin)],
)
def atualizar_produto(prod_id: int, prod: ProdutoUpdate, db: Session = Depends(get_db)):
    db_prod = db.query(Produto).filter(Produto.id == prod_id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Não encontrado")

    prod_data = prod.model_dump(exclude={"adicionais_ids"}, exclude_unset=True)
    for key, value in prod_data.items():
        setattr(db_prod, key, value)

    if prod.adicionais_ids is not None:
        db_prod.adicionais.clear()
        adcs = db.query(Adicional).filter(Adicional.id.in_(prod.adicionais_ids)).all()
        db_prod.adicionais = adcs

    db.commit()
    db.refresh(db_prod)
    return db_prod


@router.delete("/produtos/{prod_id}", dependencies=[Depends(get_current_admin)])
def inativar_produto(prod_id: int, db: Session = Depends(get_db)):
    db_prod = db.query(Produto).filter(Produto.id == prod_id).first()
    if db_prod:
        db_prod.ativo = False
        db.commit()
    return {"msg": "Inativado com sucesso"}


# ==========================================
# ADICIONAIS
# ==========================================
@router.get("/adicionais", response_model=List[AdicionalResponse])
def listar_adicionais(db: Session = Depends(get_db)):
    return db.query(Adicional).all()


@router.post(
    "/adicionais",
    response_model=AdicionalResponse,
    dependencies=[Depends(get_current_admin)],
)
def criar_adicional(item: AdicionalCreate, db: Session = Depends(get_db)):
    db_item = Adicional(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put(
    "/adicionais/{item_id}",
    response_model=AdicionalResponse,
    dependencies=[Depends(get_current_admin)],
)
def atualizar_adicional(
    item_id: int, item: AdicionalCreate, db: Session = Depends(get_db)
):
    db_item = db.query(Adicional).filter(Adicional.id == item_id).first()
    if db_item:
        for k, v in item.model_dump().items():
            setattr(db_item, k, v)
        db.commit()
        db.refresh(db_item)
    return db_item


# ==========================================
# BORDAS RECHEADAS
# ==========================================
@router.get("/tipo-bordas", response_model=List[TipoBordaResponse])
def listar_bordas(db: Session = Depends(get_db)):
    return db.query(TipoBorda).all()


@router.post(
    "/tipo-bordas",
    response_model=TipoBordaResponse,
    dependencies=[Depends(get_current_admin)],
)
def criar_borda(item: TipoBordaCreate, db: Session = Depends(get_db)):
    db_item = TipoBorda(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put(
    "/tipo-bordas/{item_id}",
    response_model=TipoBordaResponse,
    dependencies=[Depends(get_current_admin)],
)
def atualizar_borda(item_id: int, item: TipoBordaCreate, db: Session = Depends(get_db)):
    db_item = db.query(TipoBorda).filter(TipoBorda.id == item_id).first()
    if db_item:
        for k, v in item.model_dump().items():
            setattr(db_item, k, v)
        db.commit()
        db.refresh(db_item)
    return db_item


# ==========================================
# LOCAIS DE PRODUÇÃO (Cozinha, Bar, etc)
# ==========================================
@router.get("/locais-producao", response_model=List[LocalProducaoResponse])
def listar_locais(db: Session = Depends(get_db)):
    return db.query(LocalProducao).all()


@router.post(
    "/locais-producao",
    response_model=LocalProducaoResponse,
    dependencies=[Depends(get_current_admin)],
)
def criar_local(item: LocalProducaoCreate, db: Session = Depends(get_db)):
    db_item = LocalProducao(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put(
    "/locais-producao/{item_id}",
    response_model=LocalProducaoResponse,
    dependencies=[Depends(get_current_admin)],
)
def atualizar_local(
    item_id: int, item: LocalProducaoCreate, db: Session = Depends(get_db)
):
    db_item = db.query(LocalProducao).filter(LocalProducao.id == item_id).first()
    if db_item:
        for k, v in item.model_dump().items():
            setattr(db_item, k, v)
        db.commit()
        db.refresh(db_item)
    return db_item
