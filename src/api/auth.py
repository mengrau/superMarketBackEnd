"""Endpoints HTTP para el recurso auth."""

from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user,
)
from core.exceptions import UnauthorizedError
from crud.usuario_crud import UsuarioCRUD
from core.config import get_db
from models import LoginRequest, TokenResponse, UsuarioRead

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    usuario = crud.autenticar_usuario(credentials.username, credentials.password)
    if not usuario:
        raise UnauthorizedError("Credenciales inválidas")

    token = create_access_token(
        data={"sub": usuario.username, "uid": str(usuario.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.get("/me", response_model=UsuarioRead)
def me(current_user=Depends(get_current_active_user)):
    return current_user
