from sqlalchemy.orm import Session
from uuid import UUID
from entities.usuario import Usuario
from auth.security import hash_password
from models import UsuarioCreate, UsuarioUpdate


def crear_usuario(db: Session, usuario: UsuarioCreate):
    nuevo_usuario = Usuario(
        username=usuario.username,
        password_hash=hash_password(usuario.password),
        id_rol=usuario.id_rol,
        estado=usuario.estado,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def obtener_usuarios(db: Session):
    return db.query(Usuario).all()


def obtener_usuario(db: Session, usuario_id: UUID):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def actualizar_usuario(db: Session, usuario_id: UUID, datos: UsuarioUpdate):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        return None
    if datos.username:
        usuario.username = datos.username
    if datos.password:
        usuario.password_hash = hash_password(datos.password)
    if datos.id_rol:
        usuario.id_rol = datos.id_rol
    if datos.estado is not None:
        usuario.estado = datos.estado
    db.commit()
    db.refresh(usuario)
    return usuario


def eliminar_usuario(db: Session, usuario_id: UUID):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        return None
    usuario.estado = False
    db.commit()
    return usuario
