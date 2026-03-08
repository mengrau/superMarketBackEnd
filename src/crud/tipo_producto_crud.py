"""
Operaciones CRUD para la entidad TipoProducto.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.tipoProducto import TipoProducto


class TipoProductoCRUD:
    """Operaciones CRUD para TipoProducto (catálogo)."""

    def __init__(self, db: Session):
        self.db = db

    def crear_tipo_producto(
        self,
        nombre: str,
        descripcion: Optional[str] = None,
    ) -> TipoProducto:
        """
        Crea un nuevo tipo de producto.

        Args:
            nombre: Nombre del tipo (único, sin importar mayúsculas).
            descripcion: Descripción opcional.

        Returns:
            Instancia creada de TipoProducto.

        Raises:
            ValueError: Si el nombre está vacío o ya existe.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del tipo de producto es obligatorio")

        if self.obtener_tipo_por_nombre(nombre):
            raise ValueError("Ya existe un tipo de producto con ese nombre")

        tipo = TipoProducto(
            nombre=nombre.strip(),
            descripcion=descripcion.strip() if descripcion else None,
        )
        self.db.add(tipo)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def obtener_tipo_producto(self, tipo_id: UUID) -> Optional[TipoProducto]:
        """Obtiene un tipo de producto por su UUID."""
        return self.db.get(TipoProducto, tipo_id)

    def obtener_tipo_por_nombre(self, nombre: str) -> Optional[TipoProducto]:
        """Obtiene un tipo de producto activo por nombre (insensible a mayúsculas)."""
        return (
            self.db.query(TipoProducto)
            .filter(
                TipoProducto.nombre.ilike((nombre or "").strip()),
                TipoProducto.estado == True,
            )
            .first()
        )

    def obtener_tipos_producto(
        self, skip: int = 0, limit: int = 100, solo_activos: bool = True
    ) -> List[TipoProducto]:
        """
        Lista tipos de producto con paginación.

        Args:
            skip: Registros a omitir.
            limit: Límite de resultados.
            solo_activos: Si True, retorna solo tipos con estado=True.
        """
        query = self.db.query(TipoProducto)
        if solo_activos:
            query = query.filter(TipoProducto.estado == True)
        return query.offset(skip).limit(limit).all()

    def actualizar_tipo_producto(
        self, tipo_id: UUID, **kwargs
    ) -> Optional[TipoProducto]:
        """
        Actualiza un tipo de producto.
        Campos soportados: nombre, descripcion, estado.

        Args:
            tipo_id: UUID del tipo de producto.
            **kwargs: Campos a actualizar.

        Returns:
            Instancia actualizada o None si no existe.

        Raises:
            ValueError: Si el nuevo nombre ya existe en otro tipo.
        """
        tipo = self.obtener_tipo_producto(tipo_id)
        if not tipo:
            return None

        if "nombre" in kwargs and kwargs["nombre"] is not None:
            existente = self.obtener_tipo_por_nombre(kwargs["nombre"])
            if existente and existente.id != tipo_id:
                raise ValueError("Ya existe un tipo de producto con ese nombre")
            kwargs["nombre"] = kwargs["nombre"].strip()

        for key, value in kwargs.items():
            if hasattr(tipo, key):
                setattr(tipo, key, value)

        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def eliminar_tipo_producto(self, tipo_id: UUID) -> bool:
        """
        Desactiva un tipo de producto (soft delete).

        Args:
            tipo_id: UUID del tipo de producto.

        Returns:
            True si se desactivó, False si no existe.
        """
        tipo = self.obtener_tipo_producto(tipo_id)
        if not tipo:
            return False
        tipo.estado = False
        self.db.commit()
        return True
