"""Entidad ORM para rol."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.config import Base


class Rol(Base):
    """
    Modelo ORM para la tabla 'roles'.
    Define los perfiles de acceso y salario base asociados a los usuarios.
    """

    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nombre = Column(String(80), nullable=False, unique=True)
    descripcion = Column(String(250))
    salario = Column(Numeric(12, 2), nullable=True)

    activo = Column(Boolean, default=True)

    fecha_creacion = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    fecha_actualizacion = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    usuarios = relationship("Usuario", back_populates="rol")

    def __repr__(self):
        """Ejecuta repr en Rol."""
        return f"<Rol {self.nombre}>"
