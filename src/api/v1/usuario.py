from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from src.database.config import get_db
from src.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from src.services.usuarioService import (
    crear_usuario,
    obtener_usuarios,
    obtener_usuario,
    actualizar_usuario,
    eliminar_usuario,
)

router = APIRouter()



@router.post("/", response_model=UsuarioResponse)
def create(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)



@router.get("/", response_model=list[UsuarioResponse])
def list_all(db: Session = Depends(get_db)):
    return obtener_usuarios(db)



@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_by_id(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario



@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update(usuario_id: UUID, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = actualizar_usuario(db, usuario_id, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario



@router.delete("/{usuario_id}")
def delete(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = eliminar_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario desactivado correctamente"}