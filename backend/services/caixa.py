"""
Manutenção e checagem do estado do Caixa.
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from models import Caixa, Sangria
from fastapi import HTTPException, status


def get_caixa_aberto(db: Session) -> Caixa:
    """Retorna o caixa atualmente aberto, se existir."""
    return db.query(Caixa).filter(Caixa.status == "Aberto").first()


def require_caixa_aberto(db: Session) -> Caixa:
    """Lança exceção se não houver caixa aberto, senão retorna o caixa."""
    caixa = get_caixa_aberto(db)
    if not caixa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum caixa aberto no momento. Abra o caixa primeiro para realizar esta operação.",
        )
    return caixa


def require_nenhum_caixa_aberto(db: Session):
    """Lança exceção se já existir um caixa aberto."""
    caixa = get_caixa_aberto(db)
    if caixa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Já existe um caixa aberto (desde {caixa.data_abertura.strftime('%d/%m/%Y %H:%M')}). Feche-o primeiro.",
        )


# Funções auxiliares para sumarizar o caixa ao fechar serão adicionadas
# no router de financeiro quando for implementar o cálculo.
