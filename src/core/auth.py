"""Funciones de autenticación, JWT y gestión de contraseñas."""

import logging
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.config import get_db
from core.exceptions import UnauthorizedError


logger = logging.getLogger(__name__)


def _normalize_bcrypt_input(password: str) -> bytes:
    """Normalizar contraseña al límite de 72 bytes requerido por bcrypt."""
    password_bytes = password.encode("utf-8")
    return password_bytes[:72]


SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY", "dev-only-change-this-secret-at-least-32-bytes"
)
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

if ALGORITHM.upper().startswith("HS") and len(SECRET_KEY.encode("utf-8")) < 32:
    logger.warning(
        "JWT_SECRET_KEY debería tener al menos 32 bytes para %s",
        ALGORITHM,
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    """Generar hash seguro de contraseña usando bcrypt nativo."""
    normalized_password = _normalize_bcrypt_input(password)

    try:
        hashed = bcrypt.hashpw(normalized_password, bcrypt.gensalt())
        return hashed.decode("utf-8")
    except Exception:
        logger.exception("Fallo al hashear contraseña")
        raise


def verify_password(password: str, hashed: str) -> bool:
    """Verificar una contraseña contra un hash almacenado."""
    if hashed.startswith("plaintext:"):
        return password == hashed.replace("plaintext:", "")

    normalized_password = _normalize_bcrypt_input(password)

    try:
        return bcrypt.checkpw(normalized_password, hashed.encode("utf-8"))
    except Exception:
        logger.exception("Fallo al verificar contraseña")
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crear un JWT firmado con fecha de expiración."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update(
        {
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Validar y decodificar un JWT."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise UnauthorizedError("Token inválido o expirado") from exc


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """Obtener el usuario autenticado a partir del token Bearer."""
    from crud.usuario_crud import UsuarioCRUD

    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise UnauthorizedError("Token sin sujeto válido")

    usuario = UsuarioCRUD(db).obtener_usuario_por_username(username)
    if not usuario:
        raise UnauthorizedError("Usuario no encontrado")

    return usuario


def get_current_active_user(current_user=Depends(get_current_user)):
    """Validar que el usuario autenticado esté activo."""
    if not current_user.estado:
        raise UnauthorizedError("Usuario inactivo")
    return current_user
