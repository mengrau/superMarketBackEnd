"""Endpoints HTTP para el recurso proveedor."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from core.config import get_db
from models import ProveedorCreate, ProveedorRead, ProveedorUpdate
from crud.proveedor_crud import ProveedorCRUD

router = APIRouter()


@router.post("/", response_model=ProveedorRead, status_code=201)
def create(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    """Ejecuta create."""
    crud = ProveedorCRUD(db)
    try:
        return crud.crear_proveedor(
            nombre=proveedor.nombre,
            nit=proveedor.nit,
            telefono=proveedor.telefono,
            direccion=proveedor.direccion,
            correo=proveedor.correo,
            id_usuario_creacion=getattr(proveedor, "id_usuario_creacion", None),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[ProveedorRead])
def list_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Ejecuta list all."""
    crud = ProveedorCRUD(db)
    return crud.obtener_proveedores(skip=skip, limit=limit)


@router.get("/{proveedor_id}", response_model=ProveedorRead)
def get_by_id(proveedor_id: UUID, db: Session = Depends(get_db)):
    """Ejecuta get by id."""
    crud = ProveedorCRUD(db)
    proveedor = crud.obtener_proveedor(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor


@router.put("/{proveedor_id}", response_model=ProveedorRead)
def update(proveedor_id: UUID, datos: ProveedorUpdate, db: Session = Depends(get_db)):
    """Ejecuta update."""
    crud = ProveedorCRUD(db)
    try:
        proveedor = crud.actualizar_proveedor(
            proveedor_id,
            id_usuario_edicion=getattr(datos, "id_usuario_edicion", None),
            **datos.model_dump(exclude_unset=True),
        )
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        return proveedor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{proveedor_id}", response_model=ProveedorRead)
def delete(proveedor_id: UUID, db: Session = Depends(get_db)):
    """Ejecuta delete."""
    crud = ProveedorCRUD(db)
    proveedor = crud.obtener_proveedor(proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    crud.eliminar_proveedor(proveedor_id)
    return proveedor
