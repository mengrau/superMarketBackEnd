#!/usr/bin/env python
"""
Script CLI para ejecutar seeders de base de datos.
Uso: python cli.py <comando>
"""

import sys
import os

# Agregar el directorio src al path para resolver imports correctamente
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))


def main():
    if len(sys.argv) < 2:
        print("Uso: python cli.py COMANDO")
        print("\nComandos disponibles:")
        print("  migrate       - Aplicar migraciones pendientes")
        print("  seed          - Ejecutar seeders para popular la BD")
        print("  bootstrap-db  - Aplicar migraciones y luego ejecutar seeders")
        sys.exit(1)

    comando = sys.argv[1]

    if comando == "migrate":
        print("Aplicando migraciones...")
        from database.bootstrap import run_migrations

        run_migrations()
    elif comando == "seed":
        print("Ejecutando seeders...")
        from database.seeders import seed_database

        seed_database()
    elif comando == "bootstrap-db":
        print("Actualizando esquema y ejecutando seeders...")
        from database.bootstrap import bootstrap_database

        bootstrap_database()
    else:
        print(f"Comando desconocido: {comando}")
        print("\nComandos disponibles:")
        print("  migrate       - Aplicar migraciones pendientes")
        print("  seed          - Ejecutar seeders para popular la BD")
        print("  bootstrap-db  - Aplicar migraciones y luego ejecutar seeders")
        sys.exit(1)


if __name__ == "__main__":
    main()
