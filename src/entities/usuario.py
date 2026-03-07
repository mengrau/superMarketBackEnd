import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.config import Base
from auth.security import hash_password, verify_password


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    id_rol = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    rol = relationship("Rol", back_populates="usuarios")
    estado = Column(Boolean, default=True)

    # discriminador de herencia
    tipo = Column(String(50))

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
    usuario_creador = relationship(
        "Usuario", foreign_keys=[id_usuario_creacion], remote_side=[id]
    )
    usuario_editor = relationship(
        "Usuario", foreign_keys=[id_usuario_edicion], remote_side=[id]
    )

    __mapper_args__ = {"polymorphic_identity": "usuario", "polymorphic_on": tipo}

    # -------- SEGURIDAD --------
    def set_password(self, password: str):
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)

    def __repr__(self):
        return f"<Usuario {self.username}>"
