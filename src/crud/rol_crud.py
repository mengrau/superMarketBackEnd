"""
Operaciones CRUD para la entidad Rol.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.rol import Rol


class RolCRUD:
    """Operaciones CRUD para Roles."""

    def __init__(self, db: Session):
        """Inicializa una instancia de RolCRUD."""
        self.db = db

    def crear_rol(
        self,
        nombre: str,
        descripcion: Optional[str] = None,
        salario: Optional[float] = None,
        activo: bool = True,
    ) -> Rol:
        """Ejecuta crear rol en RolCRUD."""
        rol = Rol(
            nombre=nombre.strip(),
            descripcion=descripcion.strip() if descripcion else None,
            salario=salario,
            activo=activo,
        )
        self.db.add(rol)
        self.db.commit()
        self.db.refresh(rol)
        return rol

    def obtener_rol(self, rol_id: UUID) -> Optional[Rol]:
        """Ejecuta obtener rol en RolCRUD."""
        return self.db.get(Rol, rol_id)

    def obtener_roles(self, skip: int = 0, limit: int = 100) -> List[Rol]:
        """Ejecuta obtener roles en RolCRUD."""
        return self.db.query(Rol).offset(skip).limit(limit).all()

    def actualizar_rol(self, rol_id: UUID, **kwargs) -> Optional[Rol]:
        """Ejecuta actualizar rol en RolCRUD."""
        rol = self.obtener_rol(rol_id)
        if not rol:
            return None

        """Actualizar campos permitidos"""
        campos_permitidos = {"nombre", "descripcion", "salario", "activo"}
        for key, value in kwargs.items():
            if key in campos_permitidos and hasattr(rol, key):
                setattr(rol, key, value)

        self.db.commit()
        self.db.refresh(rol)
        return rol

    def eliminar_rol(self, rol_id: UUID) -> bool:
        """Soft delete de rol (cambia activo a False)."""
        rol = self.obtener_rol(rol_id)
        if not rol:
            return False

        rol.activo = False
        self.db.commit()
        return True
