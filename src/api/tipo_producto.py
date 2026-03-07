from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from database.config import get_db
from models import TipoProductoCreate, TipoProductoRead, TipoProductoUpdate
from crud.tipo_producto_crud import TipoProductoCRUD

router = APIRouter()


@router.post("/", response_model=TipoProductoRead)
def create(tipo: TipoProductoCreate, db: Session = Depends(get_db)):
    crud = TipoProductoCRUD(db)
    try:
        return crud.crear_tipo_producto(
            nombre=tipo.nombre,
            descripcion=tipo.descripcion,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[TipoProductoRead])
def list_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    crud = TipoProductoCRUD(db)
    return crud.obtener_tipos_producto(skip=skip, limit=limit)


@router.get("/{tipo_id}", response_model=TipoProductoRead)
def get_by_id(tipo_id: UUID, db: Session = Depends(get_db)):
    crud = TipoProductoCRUD(db)
    tipo = crud.obtener_tipo_producto(tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return tipo


@router.put("/{tipo_id}", response_model=TipoProductoRead)
def update(tipo_id: UUID, datos: TipoProductoUpdate, db: Session = Depends(get_db)):
    crud = TipoProductoCRUD(db)
    try:
        tipo = crud.actualizar_tipo_producto(
            tipo_id,
            **datos.model_dump(exclude_unset=True),
        )
        if not tipo:
            raise HTTPException(
                status_code=404, detail="Tipo de producto no encontrado"
            )
        return tipo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{tipo_id}", response_model=TipoProductoRead)
def delete(tipo_id: UUID, db: Session = Depends(get_db)):
    crud = TipoProductoCRUD(db)
    tipo = crud.obtener_tipo_producto(tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    crud.eliminar_tipo_producto(tipo_id)
    return tipo
