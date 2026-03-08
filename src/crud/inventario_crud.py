"""
Operaciones CRUD para la entidad Inventario.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.inventario import Inventario
from entities.producto import Producto
from entities.sucursal import Sucursal


class InventarioCRUD:
    """Operaciones CRUD para Inventarios."""

    def __init__(self, db: Session):
        self.db = db

    def crear_inventario(
        self,
        id_producto: UUID,
        id_sucursal: UUID,
        stock_actual: int = 0,
        stock_minimo: int = 0,
        ubicacion: Optional[str] = None,
        id_usuario_creacion: Optional[UUID] = None,
    ) -> Inventario:
        """
        Crea un registro de inventario para un producto en una sucursal.

        Args:
            id_producto: UUID del producto.
            id_sucursal: UUID de la sucursal.
            stock_actual: Stock inicial (por defecto 0).
            stock_minimo: Stock mínimo de alerta (por defecto 0).
            ubicacion: Ubicación física en la sucursal (opcional).
            id_usuario_creacion: UUID del usuario que crea el registro (opcional).

        Returns:
            Instancia creada de Inventario.

        Raises:
            ValueError: Si las FK no existen, los valores son inválidos o
                        ya existe un inventario para esa combinación producto-sucursal.
        """
        if stock_actual < 0:
            raise ValueError("El stock actual no puede ser negativo")
        if stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo")

        if self.db.get(Producto, id_producto) is None:
            raise ValueError("El producto especificado no existe")
        if self.db.get(Sucursal, id_sucursal) is None:
            raise ValueError("La sucursal especificada no existe")

        if self.obtener_inventario_por_producto_sucursal(id_producto, id_sucursal):
            raise ValueError(
                "Ya existe un inventario para ese producto en esa sucursal"
            )

        inventario = Inventario(
            id_producto=id_producto,
            id_sucursal=id_sucursal,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo,
            ubicacion=ubicacion.strip() if ubicacion else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(inventario)
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def obtener_inventario(self, inventario_id: UUID) -> Optional[Inventario]:
        """Obtiene un registro de inventario por su UUID."""
        return self.db.get(Inventario, inventario_id)

    def obtener_inventario_por_producto_sucursal(
        self, id_producto: UUID, id_sucursal: UUID
    ) -> Optional[Inventario]:
        """Obtiene el inventario de un producto en una sucursal específica."""
        return (
            self.db.query(Inventario)
            .filter(
                Inventario.id_producto == id_producto,
                Inventario.id_sucursal == id_sucursal,
            )
            .first()
        )

    def obtener_inventarios(
        self, skip: int = 0, limit: int = 100, solo_activos: bool = True
    ) -> List[Inventario]:
        """Lista todos los registros de inventario con paginación."""
        query = self.db.query(Inventario)
        if solo_activos:
            query = query.filter(Inventario.estado == True)
        return query.offset(skip).limit(limit).all()

    def obtener_inventarios_por_sucursal(
        self, id_sucursal: UUID, skip: int = 0, limit: int = 100
    ) -> List[Inventario]:
        """Lista el inventario completo de una sucursal."""
        return (
            self.db.query(Inventario)
            .filter(Inventario.id_sucursal == id_sucursal, Inventario.estado == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_inventarios_bajo_minimo(
        self, id_sucursal: Optional[UUID] = None
    ) -> List[Inventario]:
        """
        Retorna los inventarios cuyo stock_actual es menor al stock_minimo.

        Args:
            id_sucursal: Si se indica, filtra por sucursal. De lo contrario retorna todos.
        """
        query = self.db.query(Inventario).filter(
            Inventario.stock_actual < Inventario.stock_minimo,
            Inventario.estado == True,
        )
        if id_sucursal:
            query = query.filter(Inventario.id_sucursal == id_sucursal)
        return query.all()

    def ajustar_stock(
        self,
        inventario_id: UUID,
        cantidad: int,
        id_usuario_edicion: Optional[UUID] = None,
    ) -> Optional[Inventario]:
        """
        Suma o resta unidades al stock_actual.

        Args:
            inventario_id: UUID del inventario.
            cantidad: Unidades a sumar (positivo) o restar (negativo).
            id_usuario_edicion: UUID del usuario que realiza el ajuste.

        Returns:
            Inventario actualizado o None si no existe.

        Raises:
            ValueError: Si el ajuste deja el stock en negativo.
        """
        inventario = self.obtener_inventario(inventario_id)
        if not inventario:
            return None

        nuevo_stock = inventario.stock_actual + cantidad
        if nuevo_stock < 0:
            raise ValueError(
                f"Stock insuficiente. Stock actual: {inventario.stock_actual}, "
                f"ajuste solicitado: {cantidad}"
            )

        inventario.stock_actual = nuevo_stock
        if id_usuario_edicion:
            inventario.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def actualizar_inventario(
        self, inventario_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Inventario]:
        """
        Actualiza un registro de inventario.
        Campos soportados: stock_actual, stock_minimo, ubicacion, estado.

        Args:
            inventario_id: UUID del inventario.
            id_usuario_edicion: UUID del usuario que edita (opcional).
            **kwargs: Campos a actualizar.

        Returns:
            Instancia actualizada o None si no existe.

        Raises:
            ValueError: Si los valores de stock son negativos.
        """
        inventario = self.obtener_inventario(inventario_id)
        if not inventario:
            return None

        if "stock_actual" in kwargs and kwargs["stock_actual"] is not None:
            if kwargs["stock_actual"] < 0:
                raise ValueError("El stock actual no puede ser negativo")
        if "stock_minimo" in kwargs and kwargs["stock_minimo"] is not None:
            if kwargs["stock_minimo"] < 0:
                raise ValueError("El stock mínimo no puede ser negativo")

        if id_usuario_edicion:
            kwargs["id_usuario_edicion"] = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(inventario, key):
                setattr(inventario, key, value)

        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def eliminar_inventario(
        self, inventario_id: UUID, id_usuario_edicion: Optional[UUID] = None
    ) -> bool:
        """
        Desactiva un registro de inventario (soft delete).

        Args:
            inventario_id: UUID del inventario.
            id_usuario_edicion: UUID del usuario que realiza la acción.

        Returns:
            True si se desactivó, False si no existe.
        """
        inventario = self.obtener_inventario(inventario_id)
        if not inventario:
            return False
        inventario.estado = False
        if id_usuario_edicion:
            inventario.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        return True
