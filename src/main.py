import uvicorn
from api import cliente
from api import empleado
from api import producto
from api import proveedor
from api import sucursal
from api import tipo_producto
from api import usuario
from database.config import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from auth.routes import router as auth_router  # Descomenta si tienes rutas de auth

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

# app.include_router(auth_router)  # Descomenta si tienes rutas de auth
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
        },
    }


def main():
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
