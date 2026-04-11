"""Entidad ORM para detalleCompra."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.config import Base


class DetalleCompra(Base):
    """
    Modelo ORM para la tabla 'detalle_compras'.
    Representa una línea de producto dentro de una CompraProveedor.
    """

    __tablename__ = "detalle_compras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    cantidad = Column(Integer, nullable=False, default=1)
    precio_compra = Column(Numeric(12, 2), nullable=False)

    id_compra = Column(
        UUID(as_uuid=True), ForeignKey("compras_proveedor.id"), nullable=False
    )
    id_producto = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)

    fecha_creacion = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    compra = relationship("CompraProveedor", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalle_compras")

    def __repr__(self):
        return f"<DetalleCompra {self.id} compra={self.id_compra}>"
