"""Modelo de Entrega e despacho de entregador."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Entrega(Base):
    __tablename__ = "entregas"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    entregador_id = Column(Integer, ForeignKey("entregadores.id"), nullable=True)
    status = Column(
        String(20), nullable=False, default="Aguardando"
    )  # Aguardando, Em Rota, Entregue, Devolvido
    saida = Column(DateTime(timezone=True), nullable=True)
    chegada = Column(DateTime(timezone=True), nullable=True)
    observacao = Column(String(200), nullable=True)

    pedido = relationship("Pedido", foreign_keys=[pedido_id])
    entregador = relationship("Entregador", foreign_keys=[entregador_id])
