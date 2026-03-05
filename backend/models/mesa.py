"""Modelo de Mesa."""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    capacidade = Column(Integer, nullable=False, default=4)
    status = Column(
        String(20), nullable=False, default="Livre"
    )  # Livre, Ocupada, Reservada, Manutenção
    ativo = Column(Boolean, default=True)

    pedidos = relationship("Pedido", back_populates="mesa")
