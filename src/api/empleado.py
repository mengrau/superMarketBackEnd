from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.empleado_crud import EmpleadoCRUD
from database.config import get_db
from models import EmpleadoCreate, EmpleadoRead, EmpleadoUpdate

router = APIRouter()


@router.post("/", response_model=EmpleadoRead)
def create(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    crud = EmpleadoCRUD(db)
    try:
        return crud.crear_empleado(
            username=empleado.username,
            password=empleado.password,
            id_rol=empleado.id_rol,
            nombre=empleado.nombre,
            tipo_identificacion=empleado.tipo_identificacion,
            identificacion=empleado.identificacion,
            telefono=empleado.telefono,
            direccion=empleado.direccion,
            cargo=empleado.cargo,
            salario=empleado.salario,
            estado=empleado.estado if empleado.estado is not None else True,
            id_usuario_creacion=empleado.id_usuario_creacion,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[EmpleadoRead])
def get_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    crud = EmpleadoCRUD(db)
    return crud.obtener_empleados(skip=skip, limit=limit)


@router.get("/{empleado_id}", response_model=EmpleadoRead)
def get_one(empleado_id: UUID, db: Session = Depends(get_db)):
    crud = EmpleadoCRUD(db)
    empleado = crud.obtener_empleado(empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


@router.put("/{empleado_id}", response_model=EmpleadoRead)
def update(empleado_id: UUID, empleado: EmpleadoUpdate, db: Session = Depends(get_db)):
    crud = EmpleadoCRUD(db)
    try:
        updated = crud.actualizar_empleado(
            empleado_id, **empleado.model_dump(exclude_unset=True)
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{empleado_id}", response_model=EmpleadoRead)
def delete(empleado_id: UUID, db: Session = Depends(get_db)):
    crud = EmpleadoCRUD(db)
    empleado = crud.obtener_empleado(empleado_id)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    crud.eliminar_empleado(empleado_id)
    return empleado
