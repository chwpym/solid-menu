"""Audit Log para ações críticas."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    acao = Column(
        String(50), nullable=False
    )  # CANCELAR_PEDIDO, APLICAR_DESCONTO, EXCLUIR_ITEM...
    tabela = Column(String(50), nullable=True)
    registro_id = Column(String(50), nullable=True)
    detalhe = Column(String(500), nullable=True)
    dados = Column(JSON, nullable=True)  # Snapshot ou valores
    data_hora = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", foreign_keys=[usuario_id])
