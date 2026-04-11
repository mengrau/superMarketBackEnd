"""
Configuración de seeders para ejecución automática en el arranque.

Puedes habilitar los seeders automáticos agregando esto a tu .env:
    RUN_SEEDERS_ON_STARTUP=true
"""

import os

from dotenv import load_dotenv

load_dotenv()


def _env_to_bool(name: str, default: bool = False) -> bool:
    """Leer variable de entorno y convertirla de forma segura a booleano."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


RUN_SEEDERS_ON_STARTUP = _env_to_bool("RUN_SEEDERS_ON_STARTUP", default=False)
