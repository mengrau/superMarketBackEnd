import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.config import Base


class Factura(Base):
    """
    Modelo ORM para la tabla 'facturas'.
    El campo 'estado' indica el ciclo de vida del documento: emitida, anulada o pendiente.
    Incluye campos de auditoría para trazabilidad de documentos fiscales.
    """

    __tablename__ = "facturas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    total = Column(Numeric(12, 2), nullable=False, default=0)
    metodo_pago = Column(String(80))

    id_cliente = Column(UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False)
    id_empleado = Column(UUID(as_uuid=True), ForeignKey("empleados.id"), nullable=False)
    id_sucursal = Column(
        UUID(as_uuid=True), ForeignKey("sucursales.id"), nullable=False
    )

    estado = Column(String(30), default="emitida")

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

    cliente = relationship("Cliente")
    empleado = relationship("Empleado", foreign_keys=[id_empleado])
    sucursal = relationship("Sucursal")
    detalles = relationship(
        "DetalleFactura", back_populates="factura", cascade="all, delete-orphan"
    )
    usuario_creador = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_editor = relationship("Usuario", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<Factura {self.id} total={self.total}>"
