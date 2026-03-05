from typing import Optional, List
from pydantic import BaseModel, condecimal


# Categorias
class CategoriaBase(BaseModel):
    nome: str
    ordem: int = 0
    ativo: bool = True


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True


# Locais de Producao
class LocalProducaoBase(BaseModel):
    nome: str
    ativo: bool = True


class LocalProducaoCreate(LocalProducaoBase):
    pass


class LocalProducaoResponse(LocalProducaoBase):
    id: int

    class Config:
        from_attributes = True


# Adicionais
class AdicionalBase(BaseModel):
    nome: str
    preco: condecimal(max_digits=10, decimal_places=2) = 0
    ativo: bool = True


class AdicionalCreate(AdicionalBase):
    pass


class AdicionalResponse(AdicionalBase):
    id: int

    class Config:
        from_attributes = True


# Bordas
class TipoBordaBase(BaseModel):
    nome: str
    preco_extra: condecimal(max_digits=10, decimal_places=2) = 0
    ativo: bool = True


class TipoBordaCreate(TipoBordaBase):
    pass


class TipoBordaResponse(TipoBordaBase):
    id: int

    class Config:
        from_attributes = True


# Produtos
class ProdutoBase(BaseModel):
    nome: str
    categoria_id: int
    local_producao_id: int
    preco: condecimal(max_digits=10, decimal_places=2)
    tempo_preparo: int = 15
    ativo: bool = True
    descricao: Optional[str] = None


class ProdutoCreate(ProdutoBase):
    adicionais_ids: List[int] = []


class ProdutoUpdate(ProdutoBase):
    adicionais_ids: Optional[List[int]] = None


class ProdutoResponse(ProdutoBase):
    id: int
    categoria: CategoriaResponse
    local_producao: LocalProducaoResponse
    adicionais: List[AdicionalResponse] = []

    class Config:
        from_attributes = True
