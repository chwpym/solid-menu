"""Modelos de Fornecedor e Importação NF-e."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String(200), nullable=False)
    nome_fantasia = Column(String(200), nullable=True)
    cnpj = Column(String(20), unique=True, nullable=False)
    telefone = Column(String(20), nullable=True)
    email = Column(String(150), nullable=True)
    endereco = Column(String(200), nullable=True)
    numero = Column(String(20), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    cep = Column(String(10), nullable=True)
    ativo = Column(Boolean, default=True)

    nfe_importadas = relationship("NfeImportacao", back_populates="fornecedor")
    contas_pagar = relationship("ContaPagar", back_populates="fornecedor")


class NfeImportacao(Base):
    __tablename__ = "nfe_importacoes"

    id = Column(Integer, primary_key=True, index=True)
    chave_acesso = Column(String(50), unique=True, nullable=False)
    numero = Column(String(20), nullable=False)
    serie = Column(String(10), nullable=True)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)
    valor_total = Column(Numeric(10, 2), nullable=False)
    data_emissao = Column(DateTime, nullable=True)
    importado_em = Column(DateTime(timezone=True), server_default=func.now())
    xml_path = Column(String(500), nullable=True)

    fornecedor = relationship(
        "Fornecedor", back_populates="nfe_importadas", foreign_keys=[fornecedor_id]
    )
