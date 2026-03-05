"""Modelo de Impressora configuráveis."""

from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Impressora(Base):
    __tablename__ = "impressoras"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False, unique=True)
    tipo = Column(
        String(50), nullable=False
    )  # termica_80, termica_58, a4_rede, a4_local
    ip = Column(String(50), nullable=True)
    porta = Column(Integer, nullable=True, default=9100)
    setor_id = Column(
        Integer, nullable=True
    )  # Referência ao LocalProducao para disparo condicional
    ativo = Column(Boolean, default=True)

    # As configurações default por tipo de documento ficarão nas Configurações
