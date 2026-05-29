"""
Operaciones CRUD para las entidades CompraProveedor y DetalleCompra.
"""

from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.compraProveedor import CompraProveedor
from entities.detalleCompra import DetalleCompra
from entities.inventario import Inventario
from entities.proveedor import Proveedor
from entities.producto import Producto

ESTADOS_COMPRA = {"pedida", "recibida", "anulada"}


class CompraProveedorCRUD:
    """Operaciones CRUD para ComprasProveedor y sus detalles."""

    def __init__(self, db: Session):
        """Inicializa una instancia de CompraProveedorCRUD."""
        self.db = db

    def _ajustar_inventario(
        self, id_producto: UUID, id_sucursal: UUID, cantidad: int
    ) -> None:
        """
        Suma o resta `cantidad` al inventario del producto en la sucursal.
        Si no existe el registro de inventario, lo crea con stock_actual = cantidad
        (solo si cantidad > 0).
        """
        inventario = (
            self.db.query(Inventario)
            .filter(
                Inventario.id_producto == id_producto,
                Inventario.id_sucursal == id_sucursal,
            )
            .first()
        )
        if inventario is None:
            if cantidad > 0:
                inventario = Inventario(
                    id_producto=id_producto,
                    id_sucursal=id_sucursal,
                    stock_actual=cantidad,
                    stock_minimo=0,
                )
                self.db.add(inventario)
        else:
            nuevo_stock = inventario.stock_actual + cantidad
            inventario.stock_actual = max(0, nuevo_stock)

    def crear_compra(
        self,
        id_proveedor: UUID,
        id_sucursal: Optional[UUID] = None,
        total_compra: Decimal = Decimal("0"),
        estado: str = "recibida",
        id_usuario_creacion: Optional[UUID] = None,
    ) -> CompraProveedor:
        """
        Registra una nueva compra a proveedor.

        Args:
            id_proveedor: UUID del proveedor.
            total_compra: Total de la compra (por defecto 0, se recalcula al agregar detalles).
            estado: Estado inicial ('pedida', 'recibida', 'anulada').
            id_usuario_creacion: UUID del usuario que crea el registro.

        Returns:
            Instancia creada de CompraProveedor.

        Raises:
            ValueError: Si el proveedor no existe o el estado es inválido.
        """
        if estado not in ESTADOS_COMPRA:
            raise ValueError(f"Estado inválido. Opciones: {ESTADOS_COMPRA}")
        if self.db.get(Proveedor, id_proveedor) is None:
            raise ValueError("El proveedor especificado no existe")

        compra = CompraProveedor(
            id_proveedor=id_proveedor,
            id_sucursal=id_sucursal,
            total_compra=total_compra,
            estado=estado,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(compra)
        self.db.commit()
        self.db.refresh(compra)
        return compra

    def obtener_compra(self, compra_id: UUID) -> Optional[CompraProveedor]:
        """Obtiene una compra por su UUID."""
        return self.db.get(CompraProveedor, compra_id)

    def obtener_compras(self, skip: int = 0, limit: int = 100) -> List[CompraProveedor]:
        """Lista todas las compras a proveedores con paginación."""
        return self.db.query(CompraProveedor).offset(skip).limit(limit).all()

    def obtener_compras_por_proveedor(
        self, id_proveedor: UUID, skip: int = 0, limit: int = 100
    ) -> List[CompraProveedor]:
        """Lista las compras realizadas a un proveedor específico."""
        return (
            self.db.query(CompraProveedor)
            .filter(CompraProveedor.id_proveedor == id_proveedor)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def actualizar_compra(
        self, compra_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[CompraProveedor]:
        """
        Actualiza una compra a proveedor.
        Campos soportados: total_compra, estado.

        Args:
            compra_id: UUID de la compra.
            id_usuario_edicion: UUID del usuario que edita.
            **kwargs: Campos a actualizar.

        Returns:
            Instancia actualizada o None si no existe.

        Raises:
            ValueError: Si el estado no es válido.
        """
        compra = self.obtener_compra(compra_id)
        if not compra:
            return None

        if "estado" in kwargs and kwargs["estado"] not in ESTADOS_COMPRA:
            raise ValueError(f"Estado inválido. Opciones: {ESTADOS_COMPRA}")

        estado_anterior = compra.estado
        nuevo_estado = kwargs.get("estado", estado_anterior)

        if id_usuario_edicion:
            kwargs["id_usuario_edicion"] = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(compra, key):
                setattr(compra, key, value)

        """Actualizar stock según la transición de estado"""
        if compra.id_sucursal and estado_anterior != nuevo_estado:
            detalles = self.obtener_detalles_por_compra(compra.id)
            if estado_anterior == "pedida" and nuevo_estado == "recibida":
                """Confirmar recepción: sumar stock"""
                for det in detalles:
                    self._ajustar_inventario(
                        det.id_producto, compra.id_sucursal, det.cantidad
                    )
            elif estado_anterior == "recibida" and nuevo_estado == "anulada":
                """Anular compra ya recibida: revertir stock"""
                for det in detalles:
                    self._ajustar_inventario(
                        det.id_producto, compra.id_sucursal, -det.cantidad
                    )

        self.db.commit()
        self.db.refresh(compra)
        return compra

    def anular_compra(
        self, compra_id: UUID, id_usuario_edicion: Optional[UUID] = None
    ) -> Optional[CompraProveedor]:
        """Anula una compra cambiando su estado a 'anulada'."""
        return self.actualizar_compra(
            compra_id, id_usuario_edicion=id_usuario_edicion, estado="anulada"
        )

    def agregar_detalle(
        self,
        id_compra: UUID,
        id_producto: UUID,
        cantidad: int,
        precio_compra: Decimal,
    ) -> DetalleCompra:
        """
        Agrega un ítem a una compra y recalcula el total.

        Args:
            id_compra: UUID de la compra destino.
            id_producto: UUID del producto comprado.
            cantidad: Unidades compradas (debe ser >= 1).
            precio_compra: Precio de compra por unidad.

        Returns:
            Instancia creada de DetalleCompra.

        Raises:
            ValueError: Si la compra o el producto no existen, o los valores son inválidos.
        """
        if cantidad < 1:
            raise ValueError("La cantidad debe ser mayor a 0")
        if Decimal(str(precio_compra)) <= 0:
            raise ValueError("El precio de compra debe ser mayor a 0")
        if self.obtener_compra(id_compra) is None:
            raise ValueError("La compra especificada no existe")
        if self.db.get(Producto, id_producto) is None:
            raise ValueError("El producto especificado no existe")

        detalle = DetalleCompra(
            id_compra=id_compra,
            id_producto=id_producto,
            cantidad=cantidad,
            precio_compra=precio_compra,
        )
        self.db.add(detalle)

        compra = self.obtener_compra(id_compra)
        subtotal = Decimal(str(precio_compra)) * cantidad
        compra.total_compra = Decimal(str(compra.total_compra or 0)) + subtotal

        """Actualizar inventario si la compra ya está recibida"""
        if compra.estado == "recibida" and compra.id_sucursal:
            self._ajustar_inventario(id_producto, compra.id_sucursal, cantidad)

        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def actualizar_detalle(
        self,
        detalle_id: UUID,
        id_usuario_edicion: Optional[UUID] = None,
        **kwargs,
    ) -> Optional[DetalleCompra]:
        """
        Actualiza un item de compra, recalcula total y ajusta stock si aplica.
        Campos soportados: id_producto, cantidad, precio_compra.
        """
        detalle = self.obtener_detalle(detalle_id)
        if not detalle:
            return None

        producto_anterior = detalle.id_producto
        cantidad_anterior = detalle.cantidad
        precio_anterior = detalle.precio_compra

        id_producto = (
            kwargs["id_producto"]
            if kwargs.get("id_producto") is not None
            else detalle.id_producto
        )
        cantidad = (
            kwargs["cantidad"] if kwargs.get("cantidad") is not None else detalle.cantidad
        )
        precio_compra = (
            kwargs["precio_compra"]
            if kwargs.get("precio_compra") is not None
            else detalle.precio_compra
        )

        if cantidad < 1:
            raise ValueError("La cantidad debe ser mayor a 0")
        if Decimal(str(precio_compra)) <= 0:
            raise ValueError("El precio de compra debe ser mayor a 0")
        if self.db.get(Producto, id_producto) is None:
            raise ValueError("El producto especificado no existe")

        subtotal_anterior = Decimal(str(precio_anterior or 0)) * cantidad_anterior
        subtotal_nuevo = Decimal(str(precio_compra)) * cantidad

        detalle.id_producto = id_producto
        detalle.cantidad = cantidad
        detalle.precio_compra = precio_compra

        compra = self.obtener_compra(detalle.id_compra)
        if compra:
            compra.total_compra = max(
                Decimal("0"),
                Decimal(str(compra.total_compra or 0))
                - subtotal_anterior
                + subtotal_nuevo,
            )
            if compra.estado == "recibida" and compra.id_sucursal:
                if producto_anterior == id_producto:
                    delta_cantidad = cantidad - cantidad_anterior
                    if delta_cantidad:
                        self._ajustar_inventario(
                            id_producto, compra.id_sucursal, delta_cantidad
                        )
                else:
                    self._ajustar_inventario(
                        producto_anterior, compra.id_sucursal, -cantidad_anterior
                    )
                    self._ajustar_inventario(
                        id_producto, compra.id_sucursal, cantidad
                    )
            if id_usuario_edicion:
                compra.id_usuario_edicion = id_usuario_edicion

        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def obtener_detalle(self, detalle_id: UUID) -> Optional[DetalleCompra]:
        """Obtiene un detalle de compra por su UUID."""
        return self.db.get(DetalleCompra, detalle_id)

    def obtener_detalles_por_compra(self, id_compra: UUID) -> List[DetalleCompra]:
        """Lista todos los detalles de una compra."""
        return (
            self.db.query(DetalleCompra)
            .filter(DetalleCompra.id_compra == id_compra)
            .order_by(DetalleCompra.fecha_creacion.asc())
            .all()
        )

    def eliminar_detalle(self, detalle_id: UUID) -> bool:
        """
        Elimina un detalle de compra y descuenta su valor del total de la compra.

        Args:
            detalle_id: UUID del detalle.

        Returns:
            True si se eliminó, False si no existe.
        """
        detalle = self.obtener_detalle(detalle_id)
        if not detalle:
            return False

        compra = self.obtener_compra(detalle.id_compra)
        if compra:
            subtotal = Decimal(str(detalle.precio_compra or 0)) * detalle.cantidad
            compra.total_compra = max(
                Decimal("0"),
                Decimal(str(compra.total_compra or 0)) - subtotal,
            )
            """Revertir stock si la compra estaba recibida"""
            if compra.estado == "recibida" and compra.id_sucursal:
                self._ajustar_inventario(
                    detalle.id_producto, compra.id_sucursal, -detalle.cantidad
                )

        self.db.delete(detalle)
        self.db.commit()
        return True
