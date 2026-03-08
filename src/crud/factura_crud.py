"""
Operaciones CRUD para las entidades Factura y DetalleFactura.
"""

from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.factura import Factura
from entities.detalleFactura import DetalleFactura
from entities.cliente import Cliente
from entities.empleado import Empleado
from entities.sucursal import Sucursal
from entities.producto import Producto

ESTADOS_FACTURA = {"emitida", "anulada", "pendiente"}


class FacturaCRUD:
    """Operaciones CRUD para Facturas y sus detalles."""

    def __init__(self, db: Session):
        self.db = db

    def crear_factura(
        self,
        id_cliente: UUID,
        id_empleado: UUID,
        id_sucursal: UUID,
        metodo_pago: Optional[str] = None,
        total: Decimal = Decimal("0"),
        estado: str = "emitida",
        id_usuario_creacion: Optional[UUID] = None,
    ) -> Factura:
        """
        Crea una nueva factura.

        Args:
            id_cliente: UUID del cliente asociado.
            id_empleado: UUID del empleado que emite la factura.
            id_sucursal: UUID de la sucursal.
            metodo_pago: Método de pago (efectivo, tarjeta, etc.).
            total: Total de la factura (por defecto 0, se recalcula al agregar detalles).
            estado: Estado inicial ('emitida', 'anulada', 'pendiente').
            id_usuario_creacion: UUID del usuario que crea el registro.

        Returns:
            Instancia creada de Factura.

        Raises:
            ValueError: Si las FK no existen o el estado es inválido.
        """
        if estado not in ESTADOS_FACTURA:
            raise ValueError(f"Estado inválido. Opciones: {ESTADOS_FACTURA}")
        if self.db.get(Cliente, id_cliente) is None:
            raise ValueError("El cliente especificado no existe")
        if self.db.get(Empleado, id_empleado) is None:
            raise ValueError("El empleado especificado no existe")
        if self.db.get(Sucursal, id_sucursal) is None:
            raise ValueError("La sucursal especificada no existe")

        factura = Factura(
            id_cliente=id_cliente,
            id_empleado=id_empleado,
            id_sucursal=id_sucursal,
            metodo_pago=metodo_pago.strip() if metodo_pago else None,
            total=total,
            estado=estado,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)
        return factura

    def obtener_factura(self, factura_id: UUID) -> Optional[Factura]:
        """Obtiene una factura por su UUID."""
        return self.db.get(Factura, factura_id)

    def obtener_facturas(self, skip: int = 0, limit: int = 100) -> List[Factura]:
        """Lista todas las facturas con paginación."""
        return self.db.query(Factura).offset(skip).limit(limit).all()

    def obtener_facturas_por_cliente(
        self, id_cliente: UUID, skip: int = 0, limit: int = 100
    ) -> List[Factura]:
        """Lista las facturas de un cliente específico."""
        return (
            self.db.query(Factura)
            .filter(Factura.id_cliente == id_cliente)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_facturas_por_sucursal(
        self, id_sucursal: UUID, skip: int = 0, limit: int = 100
    ) -> List[Factura]:
        """Lista las facturas de una sucursal específica."""
        return (
            self.db.query(Factura)
            .filter(Factura.id_sucursal == id_sucursal)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def actualizar_factura(
        self, factura_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Factura]:
        """
        Actualiza una factura.
        Campos soportados: metodo_pago, total, estado.

        Args:
            factura_id: UUID de la factura.
            id_usuario_edicion: UUID del usuario que edita.
            **kwargs: Campos a actualizar.

        Returns:
            Instancia actualizada o None si no existe.

        Raises:
            ValueError: Si el estado no es válido.
        """
        factura = self.obtener_factura(factura_id)
        if not factura:
            return None

        if "estado" in kwargs and kwargs["estado"] not in ESTADOS_FACTURA:
            raise ValueError(f"Estado inválido. Opciones: {ESTADOS_FACTURA}")

        if id_usuario_edicion:
            kwargs["id_usuario_edicion"] = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(factura, key):
                setattr(factura, key, value)

        self.db.commit()
        self.db.refresh(factura)
        return factura

    def anular_factura(
        self, factura_id: UUID, id_usuario_edicion: Optional[UUID] = None
    ) -> Optional[Factura]:
        """Anula una factura cambiando su estado a 'anulada'."""
        return self.actualizar_factura(
            factura_id, id_usuario_edicion=id_usuario_edicion, estado="anulada"
        )

    def agregar_detalle(
        self,
        id_factura: UUID,
        id_producto: UUID,
        cantidad: int,
        precio_unitario: Decimal,
        id_usuario_creacion: Optional[UUID] = None,
    ) -> DetalleFactura:
        """
        Agrega un ítem a una factura y recalcula el total.

        Args:
            id_factura: UUID de la factura destino.
            id_producto: UUID del producto.
            cantidad: Unidades vendidas (debe ser >= 1).
            precio_unitario: Precio por unidad.
            id_usuario_creacion: UUID del usuario que agrega el detalle.

        Returns:
            Instancia creada de DetalleFactura.

        Raises:
            ValueError: Si la factura o el producto no existen, o los valores son inválidos.
        """
        if cantidad < 1:
            raise ValueError("La cantidad debe ser mayor a 0")
        if Decimal(str(precio_unitario)) <= 0:
            raise ValueError("El precio unitario debe ser mayor a 0")
        if self.obtener_factura(id_factura) is None:
            raise ValueError("La factura especificada no existe")
        if self.db.get(Producto, id_producto) is None:
            raise ValueError("El producto especificado no existe")

        subtotal = Decimal(str(precio_unitario)) * cantidad
        detalle = DetalleFactura(
            id_factura=id_factura,
            id_producto=id_producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal,
        )
        self.db.add(detalle)

        factura = self.obtener_factura(id_factura)
        factura.total = Decimal(str(factura.total or 0)) + subtotal
        if id_usuario_creacion:
            factura.id_usuario_edicion = id_usuario_creacion

        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def obtener_detalle(self, detalle_id: UUID) -> Optional[DetalleFactura]:
        """Obtiene un detalle de factura por su UUID."""
        return self.db.get(DetalleFactura, detalle_id)

    def obtener_detalles_por_factura(self, id_factura: UUID) -> List[DetalleFactura]:
        """Lista todos los detalles de una factura."""
        return (
            self.db.query(DetalleFactura)
            .filter(DetalleFactura.id_factura == id_factura)
            .all()
        )

    def eliminar_detalle(self, detalle_id: UUID) -> bool:
        """
        Elimina un detalle de factura y descuenta su subtotal del total de la factura.

        Args:
            detalle_id: UUID del detalle.

        Returns:
            True si se eliminó, False si no existe.
        """
        detalle = self.obtener_detalle(detalle_id)
        if not detalle:
            return False

        factura = self.obtener_factura(detalle.id_factura)
        if factura:
            factura.total = max(
                Decimal("0"),
                Decimal(str(factura.total or 0)) - Decimal(str(detalle.subtotal or 0)),
            )

        self.db.delete(detalle)
        self.db.commit()
        return True
