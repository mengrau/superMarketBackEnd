"""Entidad ORM para producto."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.config import Base


class Producto(Base):
    """
    Modelo ORM para la tabla 'productos'.
    Implementa soft-delete mediante la columna 'estado'.
    """

    __tablename__ = "productos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nombre = Column(String(200), nullable=False)
    codigo_barras = Column(String(100), nullable=True)
    precio_venta = Column(Numeric(12, 2), nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=True)

    id_tipo = Column(UUID(as_uuid=True), ForeignKey("tipo_productos.id"), nullable=True)
    id_proveedor = Column(
        UUID(as_uuid=True), ForeignKey("proveedores.id"), nullable=True
    )

    estado = Column(Boolean, default=True)

    fecha_creacion = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    fecha_actualizacion = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    id_usuario_creacion = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    id_usuario_edicion = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))

    tipo = relationship("TipoProducto", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    inventarios = relationship(
        "Inventario", back_populates="producto", cascade="all, delete-orphan"
    )
    detalle_facturas = relationship(
        "DetalleFactura", back_populates="producto", cascade="all, delete-orphan"
    )
    detalle_compras = relationship(
        "DetalleCompra", back_populates="producto", cascade="all, delete-orphan"
    )

    usuario_creador = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_editor = relationship("Usuario", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<Producto {self.nombre}>"
