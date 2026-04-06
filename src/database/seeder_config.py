"""
Configuración de seeders para ejecución automática en el arranque.

Puedes habilitar los seeders automáticos agregando esto a tu .env:
    RUN_SEEDERS_ON_STARTUP=true
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Leer la variable de entorno (por defecto: False para seguridad)
RUN_SEEDERS_ON_STARTUP = os.getenv("RUN_SEEDERS_ON_STARTUP", "false").lower() == "true"
