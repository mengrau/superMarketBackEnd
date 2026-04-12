"""
Operaciones CRUD para la entidad Producto.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.producto import Producto
from entities.tipoProducto import TipoProducto
from entities.proveedor import Proveedor


class ProductoCRUD:
    """Operaciones CRUD para Productos."""

    def __init__(self, db: Session):
        """Inicializa una instancia de ProductoCRUD."""
        self.db = db

    def crear_producto(
        self,
        nombre: str,
        precio_venta: Decimal,
        codigo_barras: Optional[str] = None,
        fecha_vencimiento: Optional[datetime] = None,
        id_tipo: Optional[UUID] = None,
        id_proveedor: Optional[UUID] = None,
        id_usuario_creacion: Optional[UUID] = None,
    ) -> Producto:
        """
        Crea un nuevo producto.

        Args:
            nombre: Nombre del producto.
            precio_venta: Precio de venta (debe ser mayor a 0).
            codigo_barras: Código de barras único (opcional).
            fecha_vencimiento: Fecha de vencimiento (opcional).
            id_tipo: UUID del tipo de producto (opcional).
            id_proveedor: UUID del proveedor (opcional).
            id_usuario_creacion: UUID del usuario que crea el registro (opcional).

        Returns:
            Instancia creada de Producto.

        Raises:
            ValueError: Si los datos son inválidos o las FK no existen.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto es obligatorio")
        if precio_venta is None or Decimal(str(precio_venta)) <= 0:
            raise ValueError("El precio de venta debe ser mayor a 0")

        if codigo_barras:
            if self.obtener_producto_por_codigo_barras(codigo_barras):
                raise ValueError("Ya existe un producto con ese código de barras")

        if id_tipo is not None and self.db.get(TipoProducto, id_tipo) is None:
            raise ValueError("El tipo de producto especificado no existe")
        if id_proveedor is not None and self.db.get(Proveedor, id_proveedor) is None:
            raise ValueError("El proveedor especificado no existe")

        producto = Producto(
            nombre=nombre.strip(),
            precio_venta=precio_venta,
            codigo_barras=codigo_barras.strip() if codigo_barras else None,
            fecha_vencimiento=fecha_vencimiento,
            id_tipo=id_tipo,
            id_proveedor=id_proveedor,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_producto(self, producto_id: UUID) -> Optional[Producto]:
        """Obtiene un producto por su UUID."""
        return self.db.get(Producto, producto_id)

    def obtener_producto_por_codigo_barras(
        self, codigo_barras: str
    ) -> Optional[Producto]:
        """Obtiene un producto activo por código de barras."""
        return (
            self.db.query(Producto)
            .filter(
                Producto.codigo_barras == (codigo_barras or "").strip(),
                Producto.estado,
            )
            .first()
        )

    def obtener_productos(
        self, skip: int = 0, limit: int = 100, solo_activos: bool = True
    ) -> List[Producto]:
        """
        Lista productos con paginación.

        Args:
            skip: Registros a omitir.
            limit: Límite de resultados.
            solo_activos: Si True, retorna solo productos con estado=True.
        """
        query = self.db.query(Producto)
        if solo_activos:
            query = query.filter(Producto.estado)
        return query.offset(skip).limit(limit).all()

    def obtener_productos_por_tipo(
        self, id_tipo: UUID, skip: int = 0, limit: int = 100
    ) -> List[Producto]:
        """Lista productos filtrados por tipo de producto."""
        return (
            self.db.query(Producto)
            .filter(Producto.id_tipo == id_tipo, Producto.estado)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_productos_por_proveedor(
        self, id_proveedor: UUID, skip: int = 0, limit: int = 100
    ) -> List[Producto]:
        """Lista productos filtrados por proveedor."""
        return (
            self.db.query(Producto)
            .filter(Producto.id_proveedor == id_proveedor, Producto.estado)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def actualizar_producto(
        self, producto_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Producto]:
        """
        Actualiza los datos de un producto.
        Campos soportados: nombre, precio_venta, codigo_barras, fecha_vencimiento,
        id_tipo, id_proveedor, estado.

        Args:
            producto_id: UUID del producto.
            id_usuario_edicion: UUID del usuario que edita (opcional).
            **kwargs: Campos a actualizar.

        Returns:
            Instancia actualizada o None si no existe.

        Raises:
            ValueError: Si los datos son inválidos o las FK no existen.
        """
        producto = self.obtener_producto(producto_id)
        if not producto:
            return None

        if "precio_venta" in kwargs and kwargs["precio_venta"] is not None:
            if Decimal(str(kwargs["precio_venta"])) <= 0:
                raise ValueError("El precio de venta debe ser mayor a 0")

        if "codigo_barras" in kwargs and kwargs["codigo_barras"] is not None:
            existente = self.obtener_producto_por_codigo_barras(kwargs["codigo_barras"])
            if existente and existente.id != producto_id:
                raise ValueError("Ya existe un producto con ese código de barras")
            kwargs["codigo_barras"] = kwargs["codigo_barras"].strip()

        if "id_tipo" in kwargs and kwargs["id_tipo"] is not None:
            if self.db.get(TipoProducto, kwargs["id_tipo"]) is None:
                raise ValueError("El tipo de producto especificado no existe")

        if "id_proveedor" in kwargs and kwargs["id_proveedor"] is not None:
            if self.db.get(Proveedor, kwargs["id_proveedor"]) is None:
                raise ValueError("El proveedor especificado no existe")

        if id_usuario_edicion:
            kwargs["id_usuario_edicion"] = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(producto, key):
                setattr(producto, key, value)

        self.db.commit()
        self.db.refresh(producto)
        return producto

    def eliminar_producto(
        self, producto_id: UUID, id_usuario_edicion: Optional[UUID] = None
    ) -> bool:
        """
        Desactiva un producto (soft delete).

        Args:
            producto_id: UUID del producto.
            id_usuario_edicion: UUID del usuario que realiza la acción.

        Returns:
            True si se desactivó, False si no existe.
        """
        producto = self.obtener_producto(producto_id)
        if not producto:
            return False
        producto.estado = False
        if id_usuario_edicion:
            producto.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        return True
