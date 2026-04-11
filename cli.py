#!/usr/bin/env python
"""
Comandos de mantenimiento para base de datos.

Uso:
    python cli.py <comando>
"""

import os
import sys
from collections.abc import Callable


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


CommandHandler = Callable[[], None]


def _print_help() -> None:
    """Mostrar ayuda de uso de la CLI."""
    print("Uso: python cli.py COMANDO")
    print("\nComandos disponibles:")
    print("  migrate       - Aplicar migraciones pendientes")
    print("  seed          - Ejecutar seeders para popular la BD")
    print("  bootstrap-db  - Aplicar migraciones y luego ejecutar seeders")


def _run_migrate() -> None:
    """Aplicar migraciones de Alembic."""
    print("Aplicando migraciones...")
    from database.bootstrap import run_migrations

    run_migrations()


def _run_seed() -> None:
    """Ejecutar seeders idempotentes."""
    print("Ejecutando seeders...")
    from database.seeders import seed_database

    seed_database()


def _run_bootstrap_db() -> None:
    """Aplicar migraciones y luego seeders."""
    print("Actualizando esquema y ejecutando seeders...")
    from database.bootstrap import bootstrap_database

    bootstrap_database()


COMMANDS: dict[str, CommandHandler] = {
    "migrate": _run_migrate,
    "seed": _run_seed,
    "bootstrap-db": _run_bootstrap_db,
}


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada de la CLI."""
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        _print_help()
        return 1

    comando = args[0]
    action = COMMANDS.get(comando)
    if action is None:
        print(f"Comando desconocido: {comando}")
        _print_help()
        return 1

    action()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
