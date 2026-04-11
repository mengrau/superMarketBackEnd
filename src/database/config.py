"""Compatibilidad: configuración de base de datos movida a core.config."""

from core.config import (  # noqa: F401
    Base,
    DATABASE_URL,
    SSL_MODE,
    SessionLocal,
    create_tables,
    engine,
    get_db,
)

__all__ = [
    "Base",
    "DATABASE_URL",
    "SSL_MODE",
    "SessionLocal",
    "create_tables",
    "engine",
    "get_db",
]
