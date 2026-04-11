"""Entidad ORM para tipoProducto."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.config import Base


class TipoProducto(Base):
    """
    Modelo ORM para la tabla 'tipo_productos'.
    Categoriza los productos del supermercado.
    """

    __tablename__ = "tipo_productos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nombre = Column(String(120), nullable=False)
    descripcion = Column(String(300))

    estado = Column(Boolean, default=True)

    fecha_creacion = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    fecha_actualizacion = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    productos = relationship("Producto", back_populates="tipo")

    def __repr__(self):
        return f"<TipoProducto {self.nombre}>"
