"""
Operaciones CRUD para la entidad Sucursal.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.sucursal import Sucursal


class SucursalCRUD:
    """Operaciones CRUD para Sucursales."""

    def __init__(self, db: Session):
        """Inicializa una instancia de SucursalCRUD."""
        self.db = db

    def crear_sucursal(
        self,
        nombre: str,
        direccion: Optional[str] = None,
        gerente: Optional[str] = None,
        telefono: Optional[str] = None,
        id_usuario_creacion: Optional[UUID] = None,
    ) -> Sucursal:
        """
        Crea una nueva sucursal.

        Args:
            nombre: Nombre de la sucursal.
            direccion: Dirección física (opcional).
            gerente: Nombre del gerente (opcional).
            telefono: Teléfono de contacto (opcional).
            id_usuario_creacion: UUID del usuario que crea el registro (opcional).

        Returns:
            Instancia creada de Sucursal.

        Raises:
            ValueError: Si el nombre está vacío o ya existe una sucursal con ese nombre.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la sucursal es obligatorio")

        if self.obtener_sucursal_por_nombre(nombre):
            raise ValueError("Ya existe una sucursal con ese nombre")

        sucursal = Sucursal(
            nombre=nombre.strip(),
            direccion=direccion.strip() if direccion else None,
            gerente=gerente.strip() if gerente else None,
            telefono=telefono.strip() if telefono else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(sucursal)
        self.db.commit()
        self.db.refresh(sucursal)
        return sucursal

    def obtener_sucursal(self, sucursal_id: UUID) -> Optional[Sucursal]:
        """Obtiene una sucursal por su UUID."""
        return self.db.get(Sucursal, sucursal_id)

    def obtener_sucursal_por_nombre(self, nombre: str) -> Optional[Sucursal]:
        """Obtiene una sucursal activa por nombre (búsqueda exacta, sin importar mayúsculas)."""
        return (
            self.db.query(Sucursal)
            .filter(
                Sucursal.nombre.ilike((nombre or "").strip()),
                Sucursal.estado,
            )
            .first()
        )

    def obtener_sucursales(
        self, skip: int = 0, limit: int = 100, solo_activas: bool = True
    ) -> List[Sucursal]:
        """
        Lista sucursales con paginación.

        Args:
            skip: Registros a omitir.
            limit: Límite de resultados.
            solo_activas: Si True, retorna solo sucursales con estado=True.
        """
        query = self.db.query(Sucursal)
        if solo_activas:
            query = query.filter(Sucursal.estado)
        return query.offset(skip).limit(limit).all()

    def actualizar_sucursal(
        self, sucursal_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Sucursal]:
        """
        Actualiza los datos de una sucursal.
        Campos soportados: nombre, direccion, gerente, telefono, estado.

        Args:
            sucursal_id: UUID de la sucursal.
            id_usuario_edicion: UUID del usuario que edita (opcional).
            **kwargs: Campos a actualizar.

        Returns:
            Instancia actualizada o None si no existe.

        Raises:
            ValueError: Si el nuevo nombre ya existe en otra sucursal.
        """
        sucursal = self.obtener_sucursal(sucursal_id)
        if not sucursal:
            return None

        if "nombre" in kwargs and kwargs["nombre"] is not None:
            existente = self.obtener_sucursal_por_nombre(kwargs["nombre"])
            if existente and existente.id != sucursal_id:
                raise ValueError("Ya existe una sucursal con ese nombre")
            kwargs["nombre"] = kwargs["nombre"].strip()

        if id_usuario_edicion:
            kwargs["id_usuario_edicion"] = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(sucursal, key):
                setattr(sucursal, key, value)

        self.db.commit()
        self.db.refresh(sucursal)
        return sucursal

    def eliminar_sucursal(
        self, sucursal_id: UUID, id_usuario_edicion: Optional[UUID] = None
    ) -> bool:
        """
        Desactiva una sucursal (soft delete).

        Args:
            sucursal_id: UUID de la sucursal.
            id_usuario_edicion: UUID del usuario que realiza la acción.

        Returns:
            True si se desactivó, False si no existe.
        """
        sucursal = self.obtener_sucursal(sucursal_id)
        if not sucursal:
            return False
        sucursal.estado = False
        if id_usuario_edicion:
            sucursal.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        return True
