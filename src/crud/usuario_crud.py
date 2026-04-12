"""
Operaciones CRUD y utilidades para la entidad Usuario.

Incluye creacion, consulta, actualizacion, eliminacion y autenticacion,
adaptado a la entidad Usuario real del proyecto (username, password_hash, id_rol).
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.rol import Rol
from entities.usuario import Usuario


class UsuarioCRUD:
    """Operaciones CRUD y autenticacion para Usuarios."""

    def __init__(self, db: Session):
        """Inicializa una instancia de UsuarioCRUD."""
        self.db = db

    def crear_usuario(
        self,
        username: str,
        password: str,
        id_rol: UUID,
        id_usuario_creacion: Optional[UUID] = None,
    ) -> Usuario:
        """
        Crea un nuevo usuario.

        Args:
            username: Nombre de usuario unico (maximo 50 caracteres).
            password: Contrasena en texto plano (sera hasheada).
            id_rol: UUID del rol asignado al usuario.
            id_usuario_creacion: UUID del usuario que crea el registro (opcional).

        Returns:
            Instancia creada de Usuario.

        Raises:
            ValueError: Si los datos son invalidos, el username ya existe
                        o el rol no existe.
        """
        if not username or not username.strip():
            raise ValueError("El username es obligatorio")
        if len(username.strip()) > 50:
            raise ValueError("El username no puede superar los 50 caracteres")
        if not password:
            raise ValueError("La contrasena es obligatoria")

        if (
            self.db.query(Usuario)
            .filter(
                Usuario.username.ilike(username.strip()),
                Usuario.estado,
            )
            .first()
        ):
            raise ValueError("El username ya esta en uso")

        if self.db.get(Rol, id_rol) is None:
            raise ValueError("El rol especificado no existe")

        usuario = Usuario(
            username=username.strip(),
            id_rol=id_rol,
            id_usuario_creacion=id_usuario_creacion,
        )
        truncated_password = password[:72]
        usuario.set_password(truncated_password)

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """Obtiene un usuario por su UUID."""
        return self.db.get(Usuario, usuario_id)

    def obtener_usuario_por_username(self, username: str) -> Optional[Usuario]:
        """Obtiene un usuario por su username (insensible a mayusculas)."""
        return (
            self.db.query(Usuario)
            .filter(Usuario.username.ilike((username or "").strip()))
            .first()
        )

    def obtener_usuarios(
        self, skip: int = 0, limit: int = 100, solo_activos: bool = True
    ) -> List[Usuario]:
        """
        Lista usuarios con paginacion.

        Args:
            skip: Registros a omitir.
            limit: Limite de resultados.
            solo_activos: Si True, retorna solo usuarios con estado=True.
        """
        query = self.db.query(Usuario)
        if solo_activos:
            query = query.filter(Usuario.estado)
        return query.offset(skip).limit(limit).all()

    def obtener_usuarios_por_rol(
        self, id_rol: UUID, skip: int = 0, limit: int = 100
    ) -> List[Usuario]:
        """Lista usuarios que tienen un rol especifico."""
        return (
            self.db.query(Usuario)
            .filter(Usuario.id_rol == id_rol, Usuario.estado)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def autenticar_usuario(self, username: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario por username y contrasena.

        Args:
            username: Nombre de usuario.
            password: Contrasena en texto plano.

        Returns:
            Instancia de Usuario si las credenciales son validas, None en caso contrario.
        """
        usuario = self.obtener_usuario_por_username(username)
        if not usuario or not usuario.estado:
            return None
        if usuario.check_password(password):
            return usuario
        return None

    def cambiar_contrasena(
        self,
        usuario_id: UUID,
        contrasena_actual: str,
        nueva_contrasena: str,
    ) -> bool:
        """
        Cambia la contrasena de un usuario tras verificar la actual.

        Args:
            usuario_id: UUID del usuario.
            contrasena_actual: Contrasena actual en texto plano.
            nueva_contrasena: Nueva contrasena en texto plano.

        Returns:
            True si se actualizo correctamente, False si el usuario no existe.

        Raises:
            ValueError: Si la contrasena actual es incorrecta o la nueva esta vacia.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False

        if not usuario.check_password(contrasena_actual):
            raise ValueError("La contrasena actual es incorrecta")
        if not nueva_contrasena:
            raise ValueError("La nueva contrasena no puede estar vacia")

        usuario.set_password(nueva_contrasena)
        self.db.commit()
        return True

    def actualizar_usuario(
        self,
        usuario_id: UUID,
        id_usuario_edicion: Optional[UUID] = None,
        **kwargs,
    ) -> Optional[Usuario]:
        """
        Actualiza los datos de un usuario.
        Campos soportados: username, id_rol, estado.
        Para cambiar contrasena use cambiar_contrasena().

        Args:
            usuario_id: UUID del usuario.
            id_usuario_edicion: UUID del usuario que edita (opcional).
            **kwargs: Campos a actualizar.

        Returns:
            Instancia actualizada o None si no existe.

        Raises:
            ValueError: Si el username ya existe en otro usuario o el rol no existe.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None

        if "username" in kwargs and kwargs["username"] is not None:
            nuevo_username = kwargs["username"].strip()
            if len(nuevo_username) > 50:
                raise ValueError("El username no puede superar los 50 caracteres")
            existente = self.obtener_usuario_por_username(nuevo_username)
            if existente and existente.id != usuario_id:
                raise ValueError("El username ya esta en uso")
            kwargs["username"] = nuevo_username

        if "id_rol" in kwargs and kwargs["id_rol"] is not None:
            if self.db.get(Rol, kwargs["id_rol"]) is None:
                raise ValueError("El rol especificado no existe")

        new_password = kwargs.pop("password", None)
        kwargs.pop("password_hash", None)

        if id_usuario_edicion:
            kwargs["id_usuario_edicion"] = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)

        if new_password:
            usuario.set_password(new_password)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(
        self, usuario_id: UUID, id_usuario_edicion: Optional[UUID] = None
    ) -> bool:
        """
        Desactiva un usuario (soft delete).

        Args:
            usuario_id: UUID del usuario.
            id_usuario_edicion: UUID del usuario que realiza la accion.

        Returns:
            True si se desactivo, False si no existe.
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False
        usuario.estado = False
        if id_usuario_edicion:
            usuario.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        return True

    def es_admin(self, usuario_id: UUID) -> bool:
        """
        Indica si un usuario tiene el rol admin.

        Args:
            usuario_id: UUID del usuario.

        Returns:
            True si su rol se llama admin (insensible a mayusculas).
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False
        rol = self.db.get(Rol, usuario.id_rol)
        return bool(rol and (rol.nombre or "").strip().lower() == "admin")
