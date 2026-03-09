"""
Punto de entrada de la aplicación SuperMarket.
Registra todos los routers de FastAPI, configura CORS, crea las tablas en el
arranque e inicia el menú de consola cuando se ejecuta directamente.
"""

import uvicorn
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
from api import detalleFactura
from api import detalleCompra
from api import rol

from database.config import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SuperMarket API",
    description="API backend para gestión de supermercado",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cliente.router, prefix="/clientes", tags=["Clientes"])
app.include_router(empleado.router, prefix="/empleados", tags=["Empleados"])
app.include_router(usuario.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(proveedor.router, prefix="/proveedores", tags=["Proveedores"])
app.include_router(producto.router, prefix="/productos", tags=["Productos"])
app.include_router(sucursal.router, prefix="/sucursales", tags=["Sucursales"])
app.include_router(
    tipo_producto.router,
    prefix="/tipos-producto",
    tags=["Tipos de Producto"],
)
app.include_router(inventario.router, prefix="/inventarios", tags=["Inventarios"])
app.include_router(
    compra_proveedor.router,
    prefix="/compras-proveedor",
    tags=["Compras Proveedor"],
)
app.include_router(factura.router, prefix="/facturas", tags=["Facturas"])
app.include_router(detalleFactura.router, prefix="/facturas", tags=["Detalle Factura"])
app.include_router(
    detalleCompra.router,
    prefix="/compras-proveedor",
    tags=["Detalle Compra"],
)
app.include_router(rol.router, prefix="/roles", tags=["Roles"])


@app.on_event("startup")
async def startup_event():
    print("Iniciando SuperMarket API...")
    print("Configurando base de datos...")
    create_tables()
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:8000/docs")


@app.get("/", tags=["raíz"])
async def root():
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


def main():
    from menu import iniciar_menu

    iniciar_menu()


if __name__ == "__main__":
    main()
