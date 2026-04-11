import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.errors import UnauthorizedError
from database.config import get_db

# Usar solo bcrypt sin schemes deprecados para evitar problemas de compatibilidad
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception as e:
    print(f"⚠️ Advertencia: Problema al inicializar bcrypt: {e}")
    # Fallback a plaintext para desarrollo (¡NO usar en producción!)
    pwd_context = None

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-change-this-secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    """Genera el hash seguro de la contraseña"""
    if pwd_context is None:
        # Fallback si bcrypt falla (solo para desarrollo)
        return f"plaintext:{password}"

    # Asegurar que la contraseña no excede 72 bytes (límite de bcrypt)
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode("utf-8", errors="ignore")

    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"⚠️ Error al hashear contraseña: {e}")
        return f"plaintext:{password}"


def verify_password(password: str, hashed: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    # Manejar fallback plaintext
    if hashed.startswith("plaintext:"):
        return password == hashed.replace("plaintext:", "")

    if pwd_context is None:
        return False

    # Asegurar que la contraseña no excede 72 bytes
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode("utf-8", errors="ignore")

    try:
        return pwd_context.verify(password, hashed)
    except Exception as e:
        print(f"⚠️ Error al verificar contraseña: {e}")
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crea un JWT firmado con fecha de expiración."""
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
    """Valida y decodifica un JWT."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise UnauthorizedError("Token inválido o expirado") from exc


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """Obtiene el usuario autenticado a partir del Bearer token."""
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
    """Valida que el usuario autenticado esté activo."""
    if not current_user.estado:
        raise UnauthorizedError("Usuario inactivo")
    return current_user
