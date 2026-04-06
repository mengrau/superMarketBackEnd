#!/usr/bin/env python
"""
Script CLI para ejecutar seeders de base de datos.
Uso: python cli.py seed
"""

import sys
import os

# Agregar el directorio src al path para resolver imports correctamente
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))


def main():
    if len(sys.argv) < 2:
        print("Uso: python cli.py COMANDO")
        print("\nComandos disponibles:")
        print("  seed     - Ejecutar seeders para popular la BD con datos de prueba")
        sys.exit(1)

    comando = sys.argv[1]

    if comando == "seed":
        print("Ejecutando seeders...")
        from database.seeders import seed_database
        seed_database()
    else:
        print(f"Comando desconocido: {comando}")
        print("\nComandos disponibles:")
        print("  seed     - Ejecutar seeders para popular la BD con datos de prueba")
        sys.exit(1)


if __name__ == "__main__":
    main()
