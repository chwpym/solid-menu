"""
Serviço para popular os dados iniciais essenciais da aplicação.
"""

from sqlalchemy.orm import Session
from models import Usuario, Categoria
from security import get_password_hash


def popular_dados_iniciais(db: Session):
    # Verifica se já existe um admin
    admin = db.query(Usuario).filter(Usuario.role == "admin").first()
    if not admin:
        # Cria o Admin default
        novo_admin = Usuario(
            nome="Administrador do Sistema",
            email="admin@sistema.com",
            senha_hash=get_password_hash(
                "admin123"
            ),  # Senha predefinida per design log
            role="admin",
            ativo=True,
        )
        db.add(novo_admin)

    # Garante ao menos uma categoria genérica
    categoria = db.query(Categoria).first()
    if not categoria:
        db.add(Categoria(nome="Diversos Gerais", ordem=99))

    db.commit()
