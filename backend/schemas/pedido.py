from typing import Optional, List
from pydantic import BaseModel, condecimal
from datetime import datetime


class ItemAdicionalBase(BaseModel):
    adicional_id: int
    quantidade: int = 1
    preco_unitario: condecimal(max_digits=10, decimal_places=2) = 0


class ItemPedidoBase(BaseModel):
    produto_id: int
    quantidade: int = 1
    preco_unitario: condecimal(max_digits=10, decimal_places=2)
    observacao: Optional[str] = None
    borda_id: Optional[int] = None
    status: str = "novo"


class ItemPedidoCreate(ItemPedidoBase):
    adicionais: List[ItemAdicionalBase] = []


class DeliveryInfoBase(BaseModel):
    endereco: str
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: str
    cidade: str
    cep: Optional[str] = None
    telefone: str
    taxa_entrega_id: Optional[int] = None
    status_pagamento: str = "pendente"


class PedidoPagamentoBase(BaseModel):
    forma_pagamento_id: int
    valor: condecimal(max_digits=10, decimal_places=2)


class PedidoCreate(BaseModel):
    tipo: str  # mesa, delivery, retirada
    cliente_id: Optional[int] = None
    mesa_id: Optional[int] = None
    observacao: Optional[str] = None
    itens: List[ItemPedidoCreate]
    delivery_info: Optional[DeliveryInfoBase] = None
    # pagamentos podem vir na criação (tipo delivery pago online) ou no fechamento


class PedidoFechamento(BaseModel):
    desconto: condecimal(max_digits=10, decimal_places=2) = 0
    pagamentos: List[PedidoPagamentoBase] = []
    forma_fechamento: str = "pago"  # pago, fiado


class ItemAdicionalResponse(ItemAdicionalBase):
    id: int

    class Config:
        from_attributes = True


class ItemPedidoResponse(ItemPedidoBase):
    id: int
    adicionais: List[ItemAdicionalResponse] = []

    class Config:
        from_attributes = True


class DeliveryInfoResponse(DeliveryInfoBase):
    pedido_id: int

    class Config:
        from_attributes = True


class PedidoPagamentoResponse(PedidoPagamentoBase):
    id: int

    class Config:
        from_attributes = True


class PedidoResponse(BaseModel):
    id: int
    tipo: str
    status: str
    cliente_id: Optional[int] = None
    mesa_id: Optional[int] = None
    usuario_id: Optional[int] = None
    valor_total: condecimal(max_digits=10, decimal_places=2)
    desconto: condecimal(max_digits=10, decimal_places=2)
    data_hora: datetime
    observacao: Optional[str] = None
    forma_fechamento: Optional[str] = None

    itens: List[ItemPedidoResponse] = []
    delivery_info: Optional[DeliveryInfoResponse] = None
    pagamentos: List[PedidoPagamentoResponse] = []

    class Config:
        from_attributes = True
