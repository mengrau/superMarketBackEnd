"""Funciones de autenticación, JWT y gestión de contraseñas."""

import logging
import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.config import get_db
from core.exceptions import UnauthorizedError


logger = logging.getLogger(__name__)


def _build_password_context() -> CryptContext | None:
    """Inicializar contexto de hashing basado en bcrypt."""
    try:
        return CryptContext(schemes=["bcrypt"], deprecated="auto")
    except Exception:
        logger.exception("No se pudo inicializar bcrypt; se habilita fallback inseguro")
        return None


def _truncate_for_bcrypt(password: str) -> str:
    """Ajustar longitud al límite de 72 bytes definido por bcrypt."""
    password_bytes = password.encode("utf-8")
    if len(password_bytes) <= 72:
        return password
    return password_bytes[:72].decode("utf-8", errors="ignore")


pwd_context = _build_password_context()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-change-this-secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    """Generar hash de contraseña con bcrypt o fallback de desarrollo."""
    if pwd_context is None:
        logger.warning("Hashing en modo fallback plaintext; no usar en producción")
        return f"plaintext:{password}"

    normalized_password = _truncate_for_bcrypt(password)

    try:
        return pwd_context.hash(normalized_password)
    except Exception:
        logger.exception("Fallo al hashear contraseña; se usa fallback plaintext")
        return f"plaintext:{password}"


def verify_password(password: str, hashed: str) -> bool:
    """Verificar una contraseña contra un hash almacenado."""
    if hashed.startswith("plaintext:"):
        return password == hashed.replace("plaintext:", "")

    if pwd_context is None:
        return False

    normalized_password = _truncate_for_bcrypt(password)

    try:
        return pwd_context.verify(normalized_password, hashed)
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
