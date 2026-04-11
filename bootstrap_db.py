"""Script para sincronizar esquema y seeders de base de datos.

Uso:
    python bootstrap_db.py
"""

import sys
from importlib import import_module
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def main() -> None:
    """Ejecutar bootstrap de base de datos (migraciones + seeders)."""
    bootstrap_module = import_module("database.bootstrap")
    bootstrap_module.bootstrap_database()
    print("Bootstrap de base de datos completado correctamente.")


if __name__ == "__main__":
    main()
