from fastapi import FastAPI
from src.api.v1 import cliente, usuario

app = FastAPI(
    title="SuperMarket API",
    version="1.0.0",
    description="API backend para gestión de supermercado"
)


@app.get("/")
def root():
    return {"message": "SuperMarket API funcionando 🚀"}


app.include_router(
    cliente.router,
    prefix="/api/v1/clientes",
    tags=["Clientes"]
)


app.include_router(
    usuario.router,
    prefix="/api/v1/usuarios",
    tags=["Usuarios"]
)