"""Modelos Financeiros: Formas de Pagamento, Taxas, Contas a Pagar, Caixa, Sangria."""

from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class FormaPagamento(Base):
    __tablename__ = "formas_pagamento"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False, unique=True)
    ativo = Column(Boolean, default=True)
    tipo_tef = Column(String(20), nullable=True)  # Dinheiro, PIX, Crédito, Débito


class TaxaEntrega(Base):
    __tablename__ = "taxas_entrega"

    id = Column(Integer, primary_key=True, index=True)
    bairro = Column(String(100), nullable=False, unique=True)
    valor = Column(Numeric(10, 2), nullable=False)
    ativo = Column(Boolean, default=True)


class ContaPagar(Base):
    __tablename__ = "contas_pagar"

    id = Column(Integer, primary_key=True, index=True)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)
    nfe_id = Column(Integer, ForeignKey("nfe_importacoes.id"), nullable=True)
    descricao = Column(String(200), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data_vencimento = Column(DateTime, nullable=False)
    data_pagamento = Column(DateTime, nullable=True)
    status = Column(
        String(20), nullable=False, default="Pendente"
    )  # Pendente, Pago, Atrasado, Cancelado
    forma_pagamento_id = Column(
        Integer, ForeignKey("formas_pagamento.id"), nullable=True
    )
    cadastrado_em = Column(DateTime(timezone=True), server_default=func.now())

    fornecedor = relationship(
        "Fornecedor", back_populates="contas_pagar", foreign_keys=[fornecedor_id]
    )
    forma_pagamento = relationship("FormaPagamento")
    # nfe referenciada por nfe_id apenas, NfeImportacao definida em fornecedor.py


class Caixa(Base):
    __tablename__ = "caixas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_abertura = Column(DateTime(timezone=True), server_default=func.now())
    fundo_inicial = Column(Numeric(10, 2), nullable=False, default=0)
    data_fechamento = Column(DateTime(timezone=True), nullable=True)
    total_esperado = Column(Numeric(10, 2), nullable=True)
    total_contado = Column(Numeric(10, 2), nullable=True)
    status = Column(String(20), nullable=False, default="Aberto")  # Aberto, Fechado

    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    sangrias = relationship("Sangria", back_populates="caixa")


class Sangria(Base):
    __tablename__ = "sangrias"

    id = Column(Integer, primary_key=True, index=True)
    caixa_id = Column(Integer, ForeignKey("caixas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    motivo = Column(String(200), nullable=False)
    data_hora = Column(DateTime(timezone=True), server_default=func.now())

    caixa = relationship("Caixa", back_populates="sangrias")
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
