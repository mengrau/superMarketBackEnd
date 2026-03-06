from sqlalchemy.orm import Session
from uuid import UUID
from entities.cliente import Cliente
from models import ClienteCreate, ClienteUpdate


def crear_cliente(db: Session, cliente_data: ClienteCreate):
    cliente = Cliente(**cliente_data.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def obtener_cliente(db: Session, cliente_id: UUID):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def listar_clientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cliente).offset(skip).limit(limit).all()


def actualizar_cliente(db: Session, cliente_id: UUID, cliente_data: ClienteUpdate):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        return None

    for key, value in cliente_data.model_dump(exclude_unset=True).items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente


def eliminar_cliente(db: Session, cliente_id: UUID):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        return None

    db.delete(cliente)
    db.commit()
    return cliente