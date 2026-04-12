"""
Operaciones CRUD para la entidad Empleado.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.empleado import Empleado
from entities.rol import Rol
from entities.usuario import Usuario


class EmpleadoCRUD:
    """Operaciones CRUD para Empleados."""

    def __init__(self, db: Session):
        """Inicializa una instancia de EmpleadoCRUD."""
        self.db = db

    def crear_empleado(
        self,
        username: str,
        password: str,
        id_rol: UUID,
        nombre: str,
        tipo_identificacion: str,
        identificacion: str,
        telefono: Optional[str] = None,
        direccion: Optional[str] = None,
        cargo: Optional[str] = None,
        salario: Optional[str] = None,
        estado: bool = True,
        id_usuario_creacion: Optional[UUID] = None,
    ) -> Empleado:
        """Ejecuta crear empleado en EmpleadoCRUD."""
        if not username or not username.strip():
            raise ValueError("El username es obligatorio")
        if len(username.strip()) > 50:
            raise ValueError("El username no puede superar los 50 caracteres")
        if not password:
            raise ValueError("La contrasena es obligatoria")
        if self.obtener_empleado_por_username(username):
            raise ValueError("El username ya esta en uso")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        if not tipo_identificacion or not tipo_identificacion.strip():
            raise ValueError("El tipo de identificacion es obligatorio")
        if not identificacion or not identificacion.strip():
            raise ValueError("La identificacion es obligatoria")
        if self.obtener_empleado_por_identificacion(identificacion):
            raise ValueError("La identificacion ya esta registrada")
        if self.db.get(Rol, id_rol) is None:
            raise ValueError("El rol especificado no existe")

        empleado = Empleado(
            username=username.strip(),
            id_rol=id_rol,
            estado=estado,
            id_usuario_creacion=id_usuario_creacion,
            nombre=nombre.strip(),
            tipo_identificacion=tipo_identificacion.strip().upper(),
            identificacion=identificacion.strip(),
            telefono=telefono.strip() if telefono else None,
            direccion=direccion.strip() if direccion else None,
            cargo=cargo.strip() if cargo else None,
            salario=salario.strip() if salario else None,
        )
        empleado.set_password(password[:72])

        self.db.add(empleado)
        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def obtener_empleado(self, empleado_id: UUID) -> Optional[Empleado]:
        """Ejecuta obtener empleado en EmpleadoCRUD."""
        return self.db.get(Empleado, empleado_id)

    def obtener_empleado_por_username(self, username: str) -> Optional[Empleado]:
        """Ejecuta obtener empleado por username en EmpleadoCRUD."""
        return (
            self.db.query(Empleado)
            .filter(Empleado.username.ilike((username or "").strip()))
            .first()
        )

    def obtener_empleado_por_identificacion(
        self, identificacion: str
    ) -> Optional[Empleado]:
        """Ejecuta obtener empleado por identificacion en EmpleadoCRUD."""
        return (
            self.db.query(Empleado)
            .filter(Empleado.identificacion == (identificacion or "").strip())
            .first()
        )

    def obtener_empleados(
        self, skip: int = 0, limit: int = 100, solo_activos: bool = True
    ) -> List[Empleado]:
        """Ejecuta obtener empleados en EmpleadoCRUD."""
        query = self.db.query(Empleado)
        if solo_activos:
            query = query.filter(Empleado.estado)
        return query.offset(skip).limit(limit).all()

    def actualizar_empleado(
        self,
        empleado_id: UUID,
        id_usuario_edicion: Optional[UUID] = None,
        **kwargs,
    ) -> Optional[Empleado]:
        """Ejecuta actualizar empleado en EmpleadoCRUD."""
        empleado = self.obtener_empleado(empleado_id)
        if not empleado:
            return None

        if "username" in kwargs and kwargs["username"] is not None:
            nuevo_username = kwargs["username"].strip()
            if len(nuevo_username) > 50:
                raise ValueError("El username no puede superar los 50 caracteres")
            existente = (
                self.db.query(Usuario)
                .filter(Usuario.username.ilike(nuevo_username))
                .first()
            )
            if existente and existente.id != empleado_id:
                raise ValueError("El username ya esta en uso")
            kwargs["username"] = nuevo_username

        if "identificacion" in kwargs and kwargs["identificacion"] is not None:
            nueva_identificacion = kwargs["identificacion"].strip()
            existente = self.obtener_empleado_por_identificacion(nueva_identificacion)
            if existente and existente.id != empleado_id:
                raise ValueError("La identificacion ya esta registrada")
            kwargs["identificacion"] = nueva_identificacion

        if "id_rol" in kwargs and kwargs["id_rol"] is not None:
            if self.db.get(Rol, kwargs["id_rol"]) is None:
                raise ValueError("El rol especificado no existe")

        new_password = kwargs.pop("password", None)
        kwargs.pop("password_hash", None)

        if id_usuario_edicion:
            kwargs["id_usuario_edicion"] = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(empleado, key):
                setattr(empleado, key, value)

        if new_password:
            empleado.set_password(new_password[:72])

        self.db.commit()
        self.db.refresh(empleado)
        return empleado

    def eliminar_empleado(
        self, empleado_id: UUID, id_usuario_edicion: Optional[UUID] = None
    ) -> bool:
        """Ejecuta eliminar empleado en EmpleadoCRUD."""
        empleado = self.obtener_empleado(empleado_id)
        if not empleado:
            return False
        empleado.estado = False
        if id_usuario_edicion:
            empleado.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        return True
