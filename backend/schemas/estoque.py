from typing import Optional, List
from pydantic import BaseModel, condecimal
from datetime import datetime


# Insumos
class InsumoBase(BaseModel):
    nome: str
    unidade: str
    estoque_minimo: condecimal(max_digits=12, decimal_places=3) = 0
    ativo: bool = True


class InsumoCreate(InsumoBase):
    # estoque inicial pode ser preenchido na criacao
    estoque_atual: condecimal(max_digits=12, decimal_places=3) = 0


class InsumoResponse(InsumoBase):
    id: int
    estoque_atual: condecimal(max_digits=12, decimal_places=3)

    class Config:
        from_attributes = True


# Receitas
class ReceitaBase(BaseModel):
    produto_id: int
    insumo_id: int
    quantidade: condecimal(max_digits=12, decimal_places=3)


class ReceitaCreate(ReceitaBase):
    pass


class ReceitaResponse(ReceitaBase):
    id: int

    class Config:
        from_attributes = True


# Entradas (Movimentação)
class EntradaEstoqueCreate(BaseModel):
    insumo_id: int
    fornecedor_id: Optional[int] = None
    nfe_id: Optional[int] = None
    quantidade: condecimal(max_digits=12, decimal_places=3)
    custo_unitario: condecimal(max_digits=10, decimal_places=2) = 0
    observacao: Optional[str] = None


class EntradaEstoqueResponse(EntradaEstoqueCreate):
    id: int
    data: datetime
    usuario_id: int

    class Config:
        from_attributes = True
