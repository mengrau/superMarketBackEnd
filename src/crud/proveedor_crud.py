"""
Operaciones CRUD para la entidad Proveedor.
"""

import re
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.proveedor import Proveedor


class ProveedorCRUD:
    """Operaciones CRUD para Proveedores."""

    def __init__(self, db: Session):
        self.db = db

    def _validar_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email or "") is not None

    def crear_proveedor(
        self,
        nombre: str,
        nit: str,
        telefono: Optional[str] = None,
        direccion: Optional[str] = None,
        correo: Optional[str] = None,
        id_usuario_creacion: Optional[UUID] = None,
    ) -> Proveedor:
        """
        Crea un nuevo proveedor.

        Args:
            nombre: Razón social o nombre del proveedor.
            nit: NIT único del proveedor.
            telefono: Teléfono de contacto (opcional).
            direccion: Dirección (opcional).
            correo: Correo electrónico (opcional).
            id_usuario_creacion: UUID del usuario que crea el registro (opcional).

        Returns:
            Instancia creada de Proveedor.

        Raises:
            ValueError: Si los datos son inválidos o el NIT ya existe.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del proveedor es obligatorio")
        if not nit or not nit.strip():
            raise ValueError("El NIT es obligatorio")
        if correo and not self._validar_email(correo):
            raise ValueError("El formato del correo es inválido")

        if self.obtener_proveedor_por_nit(nit):
            raise ValueError("Ya existe un proveedor con ese NIT")

        proveedor = Proveedor(
            nombre=nombre.strip(),
            nit=nit.strip(),
            telefono=telefono.strip() if telefono else None,
            direccion=direccion.strip() if direccion else None,
            correo=correo.lower().strip() if correo else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(proveedor)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def obtener_proveedor(self, proveedor_id: UUID) -> Optional[Proveedor]:
        """Obtiene un proveedor por su UUID."""
        return self.db.get(Proveedor, proveedor_id)

    def obtener_proveedor_por_nit(self, nit: str) -> Optional[Proveedor]:
        """Obtiene un proveedor activo por su NIT."""
        return (
            self.db.query(Proveedor)
            .filter(
                Proveedor.nit == (nit or "").strip(),
                Proveedor.estado == True,
            )
            .first()
        )

    def obtener_proveedores(
        self, skip: int = 0, limit: int = 100, solo_activos: bool = True
    ) -> List[Proveedor]:
        """
        Lista proveedores con paginación.

        Args:
            skip: Registros a omitir.
            limit: Límite de resultados.
            solo_activos: Si True, retorna solo proveedores con estado=True.
        """
        query = self.db.query(Proveedor)
        if solo_activos:
            query = query.filter(Proveedor.estado == True)
        return query.offset(skip).limit(limit).all()

    def actualizar_proveedor(
        self, proveedor_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Proveedor]:
        """
        Actualiza los datos de un proveedor.
        Campos soportados: nombre, nit, telefono, direccion, correo, estado.

        Args:
            proveedor_id: UUID del proveedor.
            id_usuario_edicion: UUID del usuario que edita (opcional).
            **kwargs: Campos a actualizar.

        Returns:
            Instancia actualizada o None si no existe.

        Raises:
            ValueError: Si los datos son inválidos.
        """
        proveedor = self.obtener_proveedor(proveedor_id)
        if not proveedor:
            return None

        if "nit" in kwargs and kwargs["nit"] is not None:
            existente = self.obtener_proveedor_por_nit(kwargs["nit"])
            if existente and existente.id != proveedor_id:
                raise ValueError("Ya existe un proveedor con ese NIT")
            kwargs["nit"] = kwargs["nit"].strip()

        if "correo" in kwargs and kwargs["correo"] is not None:
            if not self._validar_email(kwargs["correo"]):
                raise ValueError("El formato del correo es inválido")
            kwargs["correo"] = kwargs["correo"].lower().strip()

        if id_usuario_edicion:
            kwargs["id_usuario_edicion"] = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(proveedor, key):
                setattr(proveedor, key, value)

        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def eliminar_proveedor(
        self, proveedor_id: UUID, id_usuario_edicion: Optional[UUID] = None
    ) -> bool:
        """
        Desactiva un proveedor (soft delete).

        Args:
            proveedor_id: UUID del proveedor.
            id_usuario_edicion: UUID del usuario que realiza la acción.

        Returns:
            True si se desactivó, False si no existe.
        """
        proveedor = self.obtener_proveedor(proveedor_id)
        if not proveedor:
            return False
        proveedor.estado = False
        if id_usuario_edicion:
            proveedor.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        return True
