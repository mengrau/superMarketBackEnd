import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.config import Base


class Sucursal(Base):
    __tablename__ = "sucursales"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nombre = Column(String(120), nullable=False)
    direccion = Column(String(200))
    gerente = Column(String(120))
    telefono = Column(String(20))

    estado = Column(Boolean, default=True)

    # auditoria
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

    # relaciones auditoria
    usuario_creador = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_editor = relationship("Usuario", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<Sucursal {self.nombre}>"
