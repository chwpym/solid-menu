"""Configurações globais do sistema."""

from sqlalchemy import Column, Integer, String, Boolean, JSON
from database import Base


class Configuracao(Base):
    """Tabela de chave-valor ou registro único para configurações do restaurante."""

    __tablename__ = "configuracoes"

    id = Column(Integer, primary_key=True, index=True)
    chave = Column(String(100), nullable=False, unique=True)
    # Valores possíveis dependendo do tipo da configuração
    valor_string = Column(String(500), nullable=True)
    valor_inteiro = Column(Integer, nullable=True)
    valor_booleano = Column(Boolean, nullable=True)
    valor_json = Column(JSON, nullable=True)
    descricao = Column(String(200), nullable=True)

    # Chaves comuns previstas:
    # - restaurante_nome
    # - restaurante_cnpj
    # - restaurante_endereco
    # - relatorio_impressora_padrao (id)
    # - comanda_impressora_padrao (id)
