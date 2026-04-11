"""Script para aplicar migraciones pendientes de base de datos.

Uso:
    python migrate_db.py
"""

import sys
from importlib import import_module
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def main() -> None:
    """Ejecutar migraciones pendientes hasta head."""
    bootstrap_module = import_module("database.bootstrap")
    bootstrap_module.run_migrations()
    print("Migraciones aplicadas correctamente.")


if __name__ == "__main__":
    main()
