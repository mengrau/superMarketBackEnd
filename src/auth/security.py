"""Compatibilidad: autenticación movida a core.auth."""

from core.auth import (  # noqa: F401
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    decode_access_token,
    get_current_active_user,
    get_current_user,
    hash_password,
    oauth2_scheme,
    pwd_context,
    verify_password,
)

__all__ = [
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "ALGORITHM",
    "SECRET_KEY",
    "create_access_token",
    "decode_access_token",
    "get_current_active_user",
    "get_current_user",
    "hash_password",
    "oauth2_scheme",
    "pwd_context",
    "verify_password",
]
