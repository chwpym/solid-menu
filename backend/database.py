"""
Configuração do banco de dados SQLAlchemy.
Usa SQLite local — create_all() no startup, sem Alembic.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import DATABASE_URL, BASE_DIR

# Garante que o diretório data/ existe
(BASE_DIR / "data").mkdir(exist_ok=True)
(BASE_DIR / "data" / "backups").mkdir(exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency para injetar sessão do banco nas rotas."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Cria todas as tabelas e popula dados iniciais se necessário."""
    import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # Popula dados pré-cadastrados na primeira execução
    from services.seed import popular_dados_iniciais

    db = SessionLocal()
    try:
        popular_dados_iniciais(db)
    finally:
        db.close()
