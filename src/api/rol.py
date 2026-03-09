from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.rol_crud import RolCRUD
from database.config import get_db
from models import (
    RolCreate,
    RolRead,
    RolUpdate,
)

router = APIRouter()


@router.post("/", response_model=RolRead)
def create(rol: RolCreate, db: Session = Depends(get_db)):
    """Crea un nuevo rol en el sistema."""
    crud = RolCRUD(db)
    try:
        nuevo_rol = crud.crear_rol(
            nombre=rol.nombre,
            descripcion=rol.descripcion,
            salario=rol.salario,
            activo=rol.activo,
        )
        return nuevo_rol
    except Exception as e:
        """Aquí asumiendo UniqueViolation etc.."""
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[RolRead])
def list_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Lista todos los roles."""
    crud = RolCRUD(db)
    return crud.obtener_roles(skip=skip, limit=limit)


@router.get("/{rol_id}", response_model=RolRead)
def get_one(rol_id: UUID, db: Session = Depends(get_db)):
    """Obtiene un rol por su UUID."""
    crud = RolCRUD(db)
    rol = crud.obtener_rol(rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@router.put("/{rol_id}", response_model=RolRead)
def update(rol_id: UUID, datos: RolUpdate, db: Session = Depends(get_db)):
    """Actualiza campos del rol."""
    crud = RolCRUD(db)
    try:
        rol = crud.actualizar_rol(rol_id, **datos.model_dump(exclude_unset=True))
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return rol
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{rol_id}")
def delete_rol(rol_id: UUID, db: Session = Depends(get_db)):
    """Desactiva un rol (Soft delete)."""
    crud = RolCRUD(db)
    ok = crud.eliminar_rol(rol_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"mensaje": "Rol desactivado correctamente"}
