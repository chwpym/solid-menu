from typing import Optional, List, Dict, Any
from pydantic import BaseModel, condecimal
from datetime import datetime


# Mesa
class MesaBase(BaseModel):
    numero: int
    capacidade: int = 4
    status: str = "Livre"
    ativo: bool = True


class MesaCreate(MesaBase):
    pass


class MesaResponse(MesaBase):
    id: int

    class Config:
        from_attributes = True


# Cliente
class ClienteBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[str] = None
    ativo: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True


# Fornecedor
class FornecedorBase(BaseModel):
    razao_social: str
    nome_fantasia: Optional[str] = None
    cnpj: str
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    ativo: bool = True


class FornecedorCreate(FornecedorBase):
    pass


class FornecedorResponse(FornecedorBase):
    id: int

    class Config:
        from_attributes = True


# Entregador
class EntregadorBase(BaseModel):
    nome: str
    telefone: Optional[str] = None
    placa_veiculo: Optional[str] = None
    tipo_veiculo: Optional[str] = None
    ativo: bool = True


class EntregadorCreate(EntregadorBase):
    pass


class EntregadorResponse(EntregadorBase):
    id: int

    class Config:
        from_attributes = True


# FormaPagamento
class FormaPagamentoBase(BaseModel):
    nome: str
    tipo_tef: Optional[str] = None
    ativo: bool = True


class FormaPagamentoCreate(FormaPagamentoBase):
    pass


class FormaPagamentoResponse(FormaPagamentoBase):
    id: int

    class Config:
        from_attributes = True


# TaxaEntrega
class TaxaEntregaBase(BaseModel):
    bairro: str
    valor: condecimal(max_digits=10, decimal_places=2)
    ativo: bool = True


class TaxaEntregaCreate(TaxaEntregaBase):
    pass


class TaxaEntregaResponse(TaxaEntregaBase):
    id: int

    class Config:
        from_attributes = True


# Impressora
class ImpressoraBase(BaseModel):
    nome: str
    tipo: str
    ip: Optional[str] = None
    porta: int = 9100
    setor_id: Optional[int] = None
    ativo: bool = True


class ImpressoraCreate(ImpressoraBase):
    pass


class ImpressoraResponse(ImpressoraBase):
    id: int

    class Config:
        from_attributes = True


# Configuracao
class ConfiguracaoBase(BaseModel):
    chave: str
    valor_string: Optional[str] = None
    valor_inteiro: Optional[int] = None
    valor_booleano: Optional[bool] = None
    valor_json: Optional[Dict[str, Any]] = None
    descricao: Optional[str] = None


class ConfiguracaoCreate(ConfiguracaoBase):
    pass


class ConfiguracaoResponse(ConfiguracaoBase):
    id: int

    class Config:
        from_attributes = True
