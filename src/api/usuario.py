"""Endpoints HTTP para el recurso usuario."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from core.config import get_db
from models import UsuarioCreate, UsuarioRead, UsuarioUpdate
from crud.usuario_crud import UsuarioCRUD
from entities.usuario import Usuario

router = APIRouter()


@router.post("/", response_model=UsuarioRead, status_code=201)
def create(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    total_usuarios = db.query(Usuario).count()
    id_usuario_creacion = None
    if total_usuarios > 0:
        raise HTTPException(
            status_code=400,
            detail="Solo puedes crear el primer usuario sin id_usuario_creacion. Para los siguientes, usa el endpoint de actualización o ajusta el modelo.",
        )
    try:
        return crud.crear_usuario(
            username=usuario.username,
            password=usuario.password,
            id_rol=usuario.id_rol,
            id_usuario_creacion=id_usuario_creacion,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[UsuarioRead])
def list_all(db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    return crud.obtener_usuarios()


@router.get("/{usuario_id}", response_model=UsuarioRead)
def get_by_id(usuario_id: UUID, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    usuario = crud.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioRead)
def update(usuario_id: UUID, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    try:
        updated = crud.actualizar_usuario(
            usuario_id, **datos.model_dump(exclude_unset=True)
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{usuario_id}", response_model=UsuarioRead)
def delete(usuario_id: UUID, db: Session = Depends(get_db)):
    crud = UsuarioCRUD(db)
    usuario = crud.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    crud.eliminar_usuario(usuario_id)
    return usuario
