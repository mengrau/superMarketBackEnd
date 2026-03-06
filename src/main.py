import uvicorn
from api.v1 import cliente, usuario
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
app.include_router(cliente.router, prefix="/api/v1/clientes", tags=["Clientes"])
app.include_router(usuario.router, prefix="/api/v1/usuarios", tags=["Usuarios"])


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
            "Clientes": "/api/v1/clientes",
            "Usuarios": "/api/v1/usuarios",
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
