"""Modelos de Pedidos: Pedido, ItemPedido, ItemAdicional, DeliveryInfo, PedidoPagamento."""

from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20), nullable=False)  # mesa, delivery, retirada
    status = Column(
        String(20), nullable=False, default="novo"
    )  # novo, enviado, preparando, pronto, entregue, cancelado
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=True)
    usuario_id = Column(
        Integer, ForeignKey("usuarios.id"), nullable=True
    )  # Garçom/Caixa que abriu
    valor_total = Column(Numeric(10, 2), nullable=False, default=0)
    desconto = Column(Numeric(10, 2), nullable=False, default=0)
    data_hora = Column(DateTime(timezone=True), server_default=func.now())
    observacao = Column(String(500), nullable=True)
    forma_fechamento = Column(String(20), nullable=True)  # pago, fiado

    cliente = relationship("Cliente", back_populates="pedidos")
    mesa = relationship("Mesa", back_populates="pedidos")
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    itens = relationship(
        "ItemPedido", back_populates="pedido", cascade="all, delete-orphan"
    )
    delivery_info = relationship(
        "DeliveryInfo",
        back_populates="pedido",
        uselist=False,
        cascade="all, delete-orphan",
    )
    pagamentos = relationship(
        "PedidoPagamento", back_populates="pedido", cascade="all, delete-orphan"
    )


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    observacao = Column(String(200), nullable=True)
    borda_id = Column(Integer, ForeignKey("tipo_bordas.id"), nullable=True)
    status = Column(
        String(20), nullable=False, default="novo"
    )  # Para KDS: novo, preparando, pronto

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", foreign_keys=[produto_id])
    borda = relationship("TipoBorda", foreign_keys=[borda_id])
    adicionais = relationship(
        "ItemAdicional", back_populates="item", cascade="all, delete-orphan"
    )


class ItemAdicional(Base):
    __tablename__ = "item_adicionais"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("itens_pedido.id"), nullable=False)
    adicional_id = Column(Integer, ForeignKey("adicionais.id"), nullable=False)
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False, default=0)

    item = relationship("ItemPedido", back_populates="adicionais")
    adicional = relationship("Adicional", foreign_keys=[adicional_id])


class DeliveryInfo(Base):
    __tablename__ = "delivery_info"

    pedido_id = Column(Integer, ForeignKey("pedidos.id"), primary_key=True)
    endereco = Column(String(200), nullable=False)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    cep = Column(String(10), nullable=True)
    telefone = Column(String(20), nullable=False)
    taxa_entrega_id = Column(Integer, ForeignKey("taxas_entrega.id"), nullable=True)
    status_pagamento = Column(
        String(20), nullable=False, default="pendente"
    )  # pendente, pago

    pedido = relationship("Pedido", back_populates="delivery_info")
    taxa_entrega = relationship("TaxaEntrega", foreign_keys=[taxa_entrega_id])


class PedidoPagamento(Base):
    __tablename__ = "pedido_pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    forma_pagamento_id = Column(
        Integer, ForeignKey("formas_pagamento.id"), nullable=False
    )
    valor = Column(Numeric(10, 2), nullable=False)

    pedido = relationship("Pedido", back_populates="pagamentos")
    forma_pagamento = relationship("FormaPagamento", foreign_keys=[forma_pagamento_id])
