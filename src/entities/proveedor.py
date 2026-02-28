import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.config import Base


class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nombre = Column(String(150), nullable=False)
    nit = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(200))
    correo = Column(String(120))

    estado = Column(Boolean, default=True)

    # auditoría
    id_usuario_creacion = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    id_usuario_edicion = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    fecha_creacion = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    fecha_actualizacion = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    usuario_creador = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_editor = relationship("Usuario", foreign_keys=[id_usuario_edicion])

    # relaciones
    productos = relationship(
        "Producto", back_populates="proveedor", cascade="all, delete-orphan"
    )
    compras = relationship(
        "CompraProveedor", back_populates="proveedor", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Proveedor {self.nombre} ({self.nit})>"
