"""Modelo de Usuário."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=True)
    senha_hash = Column(String(255), nullable=True)  # Apenas admin/caixa
    pin = Column(String(10), nullable=True)  # Apenas garçom/entregador/cozinha
    role = Column(String(20), nullable=False)  # admin|caixa|garcom|entregador|cozinha
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())
