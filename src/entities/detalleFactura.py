import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.config import Base


class DetalleFactura(Base):
    __tablename__ = "detalle_facturas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(12, 2), nullable=False)
    subtotal = Column(Numeric(14, 2), nullable=False)

    id_factura = Column(UUID(as_uuid=True), ForeignKey("facturas.id"), nullable=False)
    id_producto = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)

    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    factura = relationship("Factura", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalle_facturas")

    def __repr__(self):
        return f"<DetalleFactura {self.id} factura={self.id_factura}>"
