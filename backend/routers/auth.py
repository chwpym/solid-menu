from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from models import Usuario
from schemas.usuario import Token, LoginRequest, UsuarioResponse
from security import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Autenticacao"])


@router.post("/login", response_model=Token)
def login_customizado(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login misto:
    - Se enviar 'email' e 'senha' -> Valida JWT padrão para Admin/Caixa
    - Se enviar 'pin' -> Valida PIN de 4-6 dígitos para Garçom/Entregador/Cozinha
    """
    if login_data.pin:
        # Modo PIN
        user = (
            db.query(Usuario)
            .filter(Usuario.pin == login_data.pin, Usuario.ativo == True)
            .first()
        )
        if not user:
            raise HTTPException(
                status_code=401, detail="PIN inválido ou usuário inativo"
            )

    elif login_data.email and login_data.senha:
        # Modo Email/Senha
        user = (
            db.query(Usuario)
            .filter(Usuario.email == login_data.email, Usuario.ativo == True)
            .first()
        )
        if (
            not user
            or not user.senha_hash
            or not verify_password(login_data.senha, user.senha_hash)
        ):
            raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    else:
        raise HTTPException(status_code=400, detail="Forneça email+senha ou PIN")

    # Gera token de 12 horas (expiração definida em config.py)
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "nome": user.nome,
        "role": user.role,
    }


@router.post("/token", response_model=Token)
def login_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Rota padrão OAuth2Bearer usada internamente pelo Swagger UI para testar a API."""
    user = (
        db.query(Usuario)
        .filter(Usuario.email == form_data.username, Usuario.ativo == True)
        .first()
    )
    if (
        not user
        or not user.senha_hash
        or not verify_password(form_data.password, user.senha_hash)
    ):
        raise HTTPException(status_code=401, detail="Credenciais incorretas")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "nome": user.nome,
        "role": user.role,
    }


@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """Retorna os dados do usuário atualmente logado."""
    return current_user
