from sqlalchemy.orm import Session
from uuid import UUID
from src.models import UsuarioBase
from src.schemas.usuario import UsuarioCreate, UsuarioUpdate



def crear_usuario(db: Session, usuario: UsuarioCreate):
    nuevo_usuario = UsuarioBase(
        username=usuario.username,
        id_rol=usuario.id_rol,
        estado=usuario.estado,
    )

    nuevo_usuario.set_password(usuario.password)

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario



def obtener_usuarios(db: Session):
    return db.query(UsuarioBase).all()



def obtener_usuario(db: Session, usuario_id: UUID):
    return db.query(UsuarioBase).filter(UsuarioBase.id == usuario_id).first()


def actualizar_usuario(db: Session, usuario_id: UUID, datos: UsuarioUpdate):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        return None

    if datos.username:
        usuario.username = datos.username

    if datos.password:
        usuario.set_password(datos.password)

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


