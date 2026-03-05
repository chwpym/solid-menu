from typing import Optional, List
from pydantic import BaseModel, condecimal
from datetime import datetime


# Conta a Pagar
class ContaPagarBase(BaseModel):
    fornecedor_id: Optional[int] = None
    nfe_id: Optional[int] = None
    descricao: str
    valor: condecimal(max_digits=10, decimal_places=2)
    data_vencimento: datetime
    status: str = "Pendente"
    forma_pagamento_id: Optional[int] = None


class ContaPagarCreate(ContaPagarBase):
    pass


class ContaPagarUpdate(ContaPagarBase):
    data_pagamento: Optional[datetime] = None


class ContaPagarResponse(ContaPagarBase):
    id: int
    data_pagamento: Optional[datetime] = None
    cadastrado_em: datetime

    class Config:
        from_attributes = True


# Sangria
class SangriaBase(BaseModel):
    valor: condecimal(max_digits=10, decimal_places=2)
    motivo: str


class SangriaCreate(SangriaBase):
    pass


class SangriaResponse(SangriaBase):
    id: int
    caixa_id: int
    usuario_id: int
    data_hora: datetime

    class Config:
        from_attributes = True


# Caixa
class CaixaBase(BaseModel):
    fundo_inicial: condecimal(max_digits=10, decimal_places=2) = 0


class CaixaCreate(CaixaBase):
    pass


class CaixaFechamento(BaseModel):
    total_contado: condecimal(max_digits=10, decimal_places=2)


class CaixaResponse(CaixaBase):
    id: int
    usuario_id: int
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
    total_esperado: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    total_contado: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    status: str
    sangrias: List[SangriaResponse] = []

    class Config:
        from_attributes = True
