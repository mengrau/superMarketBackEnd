from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database.config import get_db
from models import (
    ClienteCreate,
    ClienteUpdate,
    ClienteRead,
)
from crud.cliente_crud import ClienteCRUD

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteRead)
def create(cliente: ClienteCreate, db: Session = Depends(get_db)):
    crud = ClienteCRUD(db)
    try:
        return crud.crear_cliente(
            nombre=cliente.nombre,
            tipo_identificacion=cliente.tipo_identificacion,
            identificacion=cliente.identificacion,
            email=cliente.email,
            telefono=cliente.telefono,
            direccion=cliente.direccion,
            id_usuario_creacion=cliente.id_usuario_creacion,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ClienteRead])
def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    crud = ClienteCRUD(db)
    return crud.obtener_clientes(skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=ClienteRead)
def get_one(cliente_id: UUID, db: Session = Depends(get_db)):
    crud = ClienteCRUD(db)
    cliente = crud.obtener_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=ClienteRead)
def update(cliente_id: UUID, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    crud = ClienteCRUD(db)
    try:
        updated = crud.actualizar_cliente(
            cliente_id, **cliente.model_dump(exclude_unset=True)
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{cliente_id}")
def delete(cliente_id: UUID, db: Session = Depends(get_db)):
    crud = ClienteCRUD(db)
    cliente = crud.obtener_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    crud.eliminar_cliente(cliente_id)
    return cliente
