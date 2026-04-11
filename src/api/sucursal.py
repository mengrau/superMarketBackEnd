"""Endpoints HTTP para el recurso sucursal."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from core.config import get_db
from models import SucursalCreate, SucursalRead, SucursalUpdate
from crud.sucursal_crud import SucursalCRUD

router = APIRouter()


@router.post("/", response_model=SucursalRead, status_code=201)
def create(sucursal: SucursalCreate, db: Session = Depends(get_db)):
    crud = SucursalCRUD(db)
    try:
        return crud.crear_sucursal(
            nombre=sucursal.nombre,
            direccion=sucursal.direccion,
            gerente=sucursal.gerente,
            telefono=sucursal.telefono,
            id_usuario_creacion=getattr(sucursal, "id_usuario_creacion", None),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[SucursalRead])
def list_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    crud = SucursalCRUD(db)
    return crud.obtener_sucursales(skip=skip, limit=limit)


@router.get("/{sucursal_id}", response_model=SucursalRead)
def get_by_id(sucursal_id: UUID, db: Session = Depends(get_db)):
    crud = SucursalCRUD(db)
    sucursal = crud.obtener_sucursal(sucursal_id)
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal


@router.put("/{sucursal_id}", response_model=SucursalRead)
def update(sucursal_id: UUID, datos: SucursalUpdate, db: Session = Depends(get_db)):
    crud = SucursalCRUD(db)
    try:
        sucursal = crud.actualizar_sucursal(
            sucursal_id,
            id_usuario_edicion=getattr(datos, "id_usuario_edicion", None),
            **datos.model_dump(exclude_unset=True),
        )
        if not sucursal:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada")
        return sucursal
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{sucursal_id}", response_model=SucursalRead)
def delete(sucursal_id: UUID, db: Session = Depends(get_db)):
    crud = SucursalCRUD(db)
    sucursal = crud.obtener_sucursal(sucursal_id)
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    crud.eliminar_sucursal(sucursal_id)
    return sucursal
