"""
Operaciones CRUD para la entidad Empleado.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.empleado import Empleado


class EmpleadoCRUD:
    """Operaciones CRUD para Empleados."""

    def __init__(self, db: Session):
        self.db = db

    def crear_empleado(self, usuario_id: UUID, cargo: str, salario: str) -> Empleado:
        empleado = Empleado(id=usuario_id, cargo=cargo, salario=salario)
        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def obtener_empleado(self, empleado_id: UUID) -> Optional[Empleado]:
        return self.db.get(Empleado, empleado_id)

    def obtener_empleados(self, skip: int = 0, limit: int = 100) -> List[Empleado]:
        return self.db.query(Empleado).offset(skip).limit(limit).all()

    def actualizar_empleado(self, empleado_id: UUID, **kwargs) -> Optional[Empleado]:
        empleado = self.obtener_empleado(empleado_id)
        if not empleado:
            return None
        for key, value in kwargs.items():
            if hasattr(empleado, key):
                setattr(empleado, key, value)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def eliminar_empleado(self, empleado_id: UUID) -> bool:
        empleado = self.obtener_empleado(empleado_id)
        if not empleado:
            return False
        self.db.delete(empleado)
        self.db.commit()
        return True
