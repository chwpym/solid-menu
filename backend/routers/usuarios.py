from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from security import get_current_admin, get_password_hash

# Apenas admins podem gerenciar usuários (RBAC)
router = APIRouter(
    prefix="/api/usuarios", tags=["Usuarios"], dependencies=[Depends(get_current_admin)]
)


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(user: UsuarioCreate, db: Session = Depends(get_db)):
    if user.email:
        existente = db.query(Usuario).filter(Usuario.email == user.email).first()
        if existente:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

    if user.pin:
        existente = db.query(Usuario).filter(Usuario.pin == user.pin).first()
        if existente:
            raise HTTPException(
                status_code=400, detail="Este PIN já está em uso por outro usuário"
            )

    novo_usuario = Usuario(
        nome=user.nome, email=user.email, role=user.role, ativo=user.ativo, pin=user.pin
    )
    if user.senha:
        novo_usuario.senha_hash = get_password_hash(user.senha)

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@router.put("/{user_id}", response_model=UsuarioResponse)
def atualizar_usuario(user_id: int, user: UsuarioUpdate, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user.email and user.email != db_user.email:
        if db.query(Usuario).filter(Usuario.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado")

    if user.pin and user.pin != db_user.pin:
        if db.query(Usuario).filter(Usuario.pin == user.pin).first():
            raise HTTPException(status_code=400, detail="PIN já em uso")

    db_user.nome = user.nome
    db_user.email = user.email
    db_user.role = user.role
    db_user.ativo = user.ativo
    db_user.pin = user.pin

    if user.senha:
        db_user.senha_hash = get_password_hash(user.senha)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def inativar_usuario(user_id: int, db: Session = Depends(get_db)):
    """Soft delete: apenas inativa para não perder histórico de pedidos vinculados."""
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Previne do admin inativar a si mesmo se for o único, mas simplificado aqui
    db_user.ativo = False
    db_user.pin = None  # Libera o PIN
    db.commit()
    return None
