"""Modelo de Entregador."""

from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Entregador(Base):
    __tablename__ = "entregadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=True)
    placa_veiculo = Column(String(10), nullable=True)
    tipo_veiculo = Column(String(20), nullable=True)  # Moto, Bicicleta, Carro
    ativo = Column(Boolean, default=True)

    # Será referenciado em tabela separada ou em DeliveryInfo
