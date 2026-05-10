"""
Punto de entrada de la aplicación SuperMarket.
Registra todos los routers de FastAPI, configura CORS, crea las tablas en el
arranque e inicia el menú de consola cuando se ejecuta directamente.
"""

import os
import logging
from contextlib import asynccontextmanager

from api import auth as auth_api
from api import cliente
from api import compra_proveedor
from api import empleado
from api import inventario
from api import producto
from api import proveedor
from api import sucursal
from api import tipo_producto
from api import usuario
from api import factura
from api import rol

from core.auth import get_current_active_user
from core.error_handlers import register_exception_handlers
from core.config import create_tables

try:
    from database.seeder_config import RUN_SEEDERS_ON_STARTUP
except ImportError:
    RUN_SEEDERS_ON_STARTUP = False
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)


def _as_bool(value: str | None, default: bool) -> bool:
    """Convertir un valor de entorno a booleano."""
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_cors_origins() -> list[str]:
    """Obtener la lista de orígenes permitidos para CORS desde variables de entorno."""
    raw_origins = os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost:4200,http://127.0.0.1:4200",
    )
    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return origins or ["http://localhost:4200"]


def _run_optional_seeders() -> None:
    """Ejecutar seeders solo cuando esta habilitado explicitamente."""
    if not RUN_SEEDERS_ON_STARTUP:
        return

    try:
        from database.seeders import seed_database

        logger.info("Ejecutando seeders de datos iniciales")
        seed_database()
    except Exception:
        logger.exception("No fue posible ejecutar los seeders en el arranque")


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Gestionar inicializacion y cierre de recursos de la aplicacion."""
    logger.info("Iniciando SuperMarket API")
    logger.info("Sincronizando esquema de base de datos")
    create_tables()
    _run_optional_seeders()
    logger.info("Sistema listo. Documentacion en /docs")
    yield
    logger.info("Cerrando SuperMarket API")


app = FastAPI(
    title="SuperMarket API",
    description="API backend para gestión de supermercado",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

register_exception_handlers(app)

cors_allow_credentials = _as_bool(os.getenv("CORS_ALLOW_CREDENTIALS"), True)
cors_origins = _get_cors_origins()

if cors_allow_credentials and "*" in cors_origins:
    cors_origins = ["http://localhost:4200", "http://127.0.0.1:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=cors_allow_credentials,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin"],
)

auth_dependencies = [Depends(get_current_active_user)]

app.include_router(auth_api.router, prefix="/auth", tags=["Auth"])
app.include_router(
    cliente.router,
    prefix="/clientes",
    tags=["Clientes"],
    dependencies=auth_dependencies,
)
app.include_router(
    empleado.router,
    prefix="/empleados",
    tags=["Empleados"],
    dependencies=auth_dependencies,
)
app.include_router(
    usuario.router,
    prefix="/usuarios",
    tags=["Usuarios"],
    dependencies=auth_dependencies,
)
app.include_router(
    proveedor.router,
    prefix="/proveedores",
    tags=["Proveedores"],
    dependencies=auth_dependencies,
)
app.include_router(
    producto.router,
    prefix="/productos",
    tags=["Productos"],
    dependencies=auth_dependencies,
)
app.include_router(
    sucursal.router,
    prefix="/sucursales",
    tags=["Sucursales"],
    dependencies=auth_dependencies,
)
app.include_router(
    tipo_producto.router,
    prefix="/tipos-producto",
    tags=["Tipos de Producto"],
    dependencies=auth_dependencies,
)
app.include_router(
    inventario.router,
    prefix="/inventarios",
    tags=["Inventarios"],
    dependencies=auth_dependencies,
)
app.include_router(
    compra_proveedor.router,
    prefix="/compras-proveedor",
    tags=["Compras Proveedor"],
    dependencies=auth_dependencies,
)
app.include_router(
    factura.router,
    prefix="/facturas",
    tags=["Facturas"],
    dependencies=auth_dependencies,
)
app.include_router(
    rol.router,
    prefix="/roles",
    tags=["Roles"],
    dependencies=auth_dependencies,
)


@app.get("/", tags=["raíz"])
async def root():
    """Retornar metadatos básicos y rutas principales de la API."""
    return {
        "mensaje": "Bienvenido a SuperMarket API",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "Clientes": "/clientes",
            "Empleados": "/empleados",
            "Usuarios": "/usuarios",
            "Proveedores": "/proveedores",
            "Productos": "/productos",
            "Sucursales": "/sucursales",
            "TiposProducto": "/tipos-producto",
            "Inventarios": "/inventarios",
            "ComprasProveedor": "/compras-proveedor",
        },
    }


def main() -> None:
    """Iniciar el menú de consola para consumir la API."""
    from menu import iniciar_menu

    iniciar_menu()


if __name__ == "__main__":
    main()
