"""
Utilitários de segurança: hashing de senhas, validação de tokens JWT e gestão de PINs.
Segue padrões da skill auth-implementation-patterns com PyJWT e Passlib.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from models import Usuario

# Esquema oauth2 (URL onde pega o token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# Configuração do bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Retorna o hash bcrypt da senha."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    """Dependency para obter o usuário atual via JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    if user is None or not user.ativo:
        raise credentials_exception
    return user


def require_roles(roles: list[str]):
    """Dependency injection para RBAC (Role-Based Access Control)."""

    def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso.",
            )
        return current_user

    return role_checker


# --- Helpers de RBAC mais comuns ---
def get_current_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    return require_roles(["admin"])(current_user)


def get_current_caixa(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    return require_roles(["admin", "caixa"])(current_user)


def get_current_garcom(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Qualquer funcionário do salão/delivery ou superior."""
    return require_roles(["admin", "caixa", "garcom", "entregador"])(current_user)
