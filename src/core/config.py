"""Configuración de SQLAlchemy para la aplicación SuperMarket."""

import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SSL_MODE = os.getenv("SSL_MODE", "require")

if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en las variables de entorno")


def _build_connect_args(database_url: str, ssl_mode: str) -> dict[str, str]:
    """Construir argumentos de conexión adicionales según el motor usado."""
    if database_url.startswith("postgresql"):
        return {"sslmode": ssl_mode}
    return {}


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args=_build_connect_args(DATABASE_URL, SSL_MODE),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Proveer una sesión de base de datos por solicitud."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Crear las tablas declaradas en los modelos ORM."""
    Base.metadata.create_all(bind=engine)
