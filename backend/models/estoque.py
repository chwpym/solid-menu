"""Modelos de Estoque: Insumo, Receita, EntradaEstoque."""

from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Insumo(Base):
    __tablename__ = "insumos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    unidade = Column(String(20), nullable=False)  # kg, g, L, ml, un
    estoque_atual = Column(Numeric(12, 3), nullable=False, default=0)
    estoque_minimo = Column(Numeric(12, 3), nullable=False, default=0)
    ativo = Column(Boolean, default=True)

    receitas = relationship("Receita", back_populates="insumo")
    entradas = relationship("EntradaEstoque", back_populates="insumo")


class Receita(Base):
    __tablename__ = "receitas"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    insumo_id = Column(Integer, ForeignKey("insumos.id"), nullable=False)
    quantidade = Column(Numeric(12, 3), nullable=False)

    produto = relationship("Produto", back_populates="receitas")
    insumo = relationship("Insumo", back_populates="receitas")


class EntradaEstoque(Base):
    __tablename__ = "entradas_estoque"

    id = Column(Integer, primary_key=True, index=True)
    insumo_id = Column(Integer, ForeignKey("insumos.id"), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)
    nfe_id = Column(Integer, ForeignKey("nfe_importacoes.id"), nullable=True)
    quantidade = Column(Numeric(12, 3), nullable=False)
    custo_unitario = Column(Numeric(10, 2), nullable=False, default=0)
    data = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    observacao = Column(String(300), nullable=True)

    insumo = relationship("Insumo", back_populates="entradas")
