"""Endpoints HTTP para el recurso auth."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import ValidationError
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


async def _parse_login_credentials(request: Request) -> LoginRequest:
    """Aceptar credenciales desde JSON o formulario OAuth2."""
    content_type = request.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        try:
            payload = await request.json()
            return LoginRequest.model_validate(payload)
        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=exc.errors(),
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="JSON inválido en la solicitud",
            ) from exc

    if (
        "application/x-www-form-urlencoded" in content_type
        or "multipart/form-data" in content_type
    ):
        form = await request.form()
        grant_type = form.get("grant_type")
        if grant_type not in (None, "", "password"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="grant_type debe ser 'password'",
            )

        try:
            return LoginRequest.model_validate(
                {
                    "username": form.get("username"),
                    "password": form.get("password"),
                }
            )
        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=exc.errors(),
            ) from exc

    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        detail=(
            "Content-Type no soportado. Use application/json "
            "o application/x-www-form-urlencoded"
        ),
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    credentials = await _parse_login_credentials(request)
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
