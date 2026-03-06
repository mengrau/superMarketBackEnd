from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database.config import get_db
from schemas.cliente import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
)
from services.clienteService import (
    crear_cliente,
    obtener_cliente,
    listar_clientes,
    actualizar_cliente,
    eliminar_cliente,
)

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse)
def create(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return crear_cliente(db, cliente)


@router.get("/", response_model=List[ClienteResponse])
def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return listar_clientes(db, skip, limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_one(cliente_id: UUID, db: Session = Depends(get_db)):
    cliente = obtener_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update(cliente_id: UUID, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    cliente_actualizado = actualizar_cliente(db, cliente_id, cliente)
    if not cliente_actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente_actualizado


@router.delete("/{cliente_id}")
def delete(cliente_id: UUID, db: Session = Depends(get_db)):
    cliente = eliminar_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado correctamente"}
