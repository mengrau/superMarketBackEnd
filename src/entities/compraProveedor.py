"""Entidad ORM para compraProveedor."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.config import Base


class CompraProveedor(Base):
    """
    Modelo ORM para la tabla 'compras_proveedor'.
    El campo 'estado' indica el ciclo de vida de la orden: pedida, recibida o anulada.
    """

    __tablename__ = "compras_proveedor"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_compra = Column(Numeric(12, 2), nullable=False, default=0)

    id_proveedor = Column(
        UUID(as_uuid=True), ForeignKey("proveedores.id"), nullable=False
    )
    id_sucursal = Column(UUID(as_uuid=True), ForeignKey("sucursales.id"), nullable=True)

    estado = Column(String(30), default="recibida")

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

    proveedor = relationship("Proveedor", back_populates="compras")
    sucursal = relationship("Sucursal")
    detalles = relationship(
        "DetalleCompra", back_populates="compra", cascade="all, delete-orphan"
    )
    usuario_creador = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_editor = relationship("Usuario", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<CompraProveedor {self.id} total={self.total_compra}>"
