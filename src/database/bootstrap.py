"""
Utilidades para actualización de esquema y carga de datos iniciales.
"""

from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migrations() -> None:
    """Aplicar migraciones pendientes hasta `head`."""
    repo_root = Path(__file__).resolve().parents[2]
    alembic_cfg = Config(str(repo_root / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")


def run_seeders() -> None:
    """Ejecutar la carga de datos iniciales."""
    from database.seeders import seed_database

    seed_database()


def bootstrap_database() -> None:
    """Sincronizar esquema y luego cargar seeders."""
    run_migrations()
    run_seeders()
