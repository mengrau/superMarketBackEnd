import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database.config import Base


class Inventario(Base):
    """
    Modelo ORM para la tabla 'inventarios'.
    Registra el stock de un producto en una sucursal específica.
    Implementa soft-delete mediante la columna 'estado'.
    """

    __tablename__ = "inventarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    stock_actual = Column(Integer, nullable=False, default=0)
    stock_minimo = Column(Integer, nullable=False, default=0)
    ubicacion = Column(String(200))

    id_producto = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)
    id_sucursal = Column(
        UUID(as_uuid=True), ForeignKey("sucursales.id"), nullable=False
    )

    estado = Column(Boolean, default=True)

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

    producto = relationship("Producto", back_populates="inventarios")
    sucursal = relationship("Sucursal")
    usuario_creador = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_editor = relationship("Usuario", foreign_keys=[id_usuario_edicion])

    def __repr__(self):
        return f"<Inventario prod={self.id_producto} suc={self.id_sucursal} stock={self.stock_actual}>"
