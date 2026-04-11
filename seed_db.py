"""Script para ejecutar seeders idempotentes de datos iniciales.

Uso:
    python seed_db.py
"""

import sys
from importlib import import_module
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


def main() -> None:
    """Ejecutar seeders idempotentes."""
    seeders_module = import_module("database.seeders")
    seeders_module.seed_database()
    print("Seeders ejecutados correctamente.")


if __name__ == "__main__":
    main()
