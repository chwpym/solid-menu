"""Modelos do Cardápio: Categoria, LocalProducao, Produto, Adicional, TipoBorda."""

from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Tabela de associação Produto <-> Adicional (m:n)
ProdutoAdicional = Table(
    "produto_adicionais",
    Base.metadata,
    Column("produto_id", Integer, ForeignKey("produtos.id"), primary_key=True),
    Column("adicional_id", Integer, ForeignKey("adicionais.id"), primary_key=True),
)


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    ordem = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)

    produtos = relationship("Produto", back_populates="categoria")


class LocalProducao(Base):
    __tablename__ = "locais_producao"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False, unique=True)
    ativo = Column(Boolean, default=True)

    produtos = relationship("Produto", back_populates="local_producao")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    local_producao_id = Column(
        Integer, ForeignKey("locais_producao.id"), nullable=False
    )
    preco = Column(Numeric(10, 2), nullable=False)
    tempo_preparo = Column(Integer, default=15)  # em minutos
    ativo = Column(Boolean, default=True)
    descricao = Column(String(500), nullable=True)

    categoria = relationship("Categoria", back_populates="produtos")
    local_producao = relationship("LocalProducao", back_populates="produtos")
    adicionais = relationship(
        "Adicional", secondary=ProdutoAdicional, back_populates="produtos"
    )
    receitas = relationship("Receita", back_populates="produto")


class Adicional(Base):
    __tablename__ = "adicionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False, default=0)
    ativo = Column(Boolean, default=True)

    produtos = relationship(
        "Produto", secondary=ProdutoAdicional, back_populates="adicionais"
    )


class TipoBorda(Base):
    __tablename__ = "tipo_bordas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco_extra = Column(Numeric(10, 2), nullable=False, default=0)
    ativo = Column(Boolean, default=True)
