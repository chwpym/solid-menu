from typing import Optional
from pydantic import BaseModel, EmailStr


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    nome: str
    role: str


class LoginRequest(BaseModel):
    # Pode ser email+senha (admin/caixa) ou apenas pin
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    pin: Optional[str] = None


# Usuario Schemas
class UsuarioBase(BaseModel):
    nome: str
    email: Optional[EmailStr] = None
    role: str  # admin, caixa, garcom, entregador, cozinha
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    senha: Optional[str] = None
    pin: Optional[str] = None


class UsuarioUpdate(UsuarioBase):
    senha: Optional[str] = None
    pin: Optional[str] = None


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
