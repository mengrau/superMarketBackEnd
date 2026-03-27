"""
Operaciones CRUD para la entidad Cliente.
"""

import re
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from entities.cliente import Cliente


class ClienteCRUD:
    """Operaciones CRUD para Clientes."""

    def __init__(self, db: Session):
        self.db = db

    def _validar_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email or "") is not None

    def _validar_identificacion(self, identificacion: str) -> bool:
        identificacion = (identificacion or "").strip()
        return len(identificacion) >= 5

    def crear_cliente(
        self,
        nombre: str,
        tipo_identificacion: str,
        identificacion: str,
        email: Optional[str] = None,
        telefono: Optional[str] = None,
        direccion: Optional[str] = None,
        id_usuario_creacion: Optional[UUID] = None,
    ) -> Cliente:
        """
        Crea un nuevo cliente con validaciones básicas.

        Args:
            nombre: Nombre completo del cliente.
            tipo_identificacion: Tipo de identificación (CC, NIT, CE, etc.).
            identificacion: Número de identificación único.
            email: Correo electrónico (opcional).
            telefono: Teléfono de contacto (opcional).
            direccion: Dirección del cliente (opcional).
            id_usuario_creacion: UUID del usuario que crea el registro (opcional).

        Returns:
            Instancia creada de Cliente.

        Raises:
            ValueError: Si los datos son inválidos o la identificación ya existe.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio")
        if not tipo_identificacion or not tipo_identificacion.strip():
            raise ValueError("El tipo de identificación es obligatorio")
        if not identificacion or not self._validar_identificacion(identificacion):
            raise ValueError("La identificación debe tener al menos 5 caracteres")
        if email and not self._validar_email(email):
            raise ValueError("El formato del email es inválido")

        if self.obtener_cliente_por_identificacion(identificacion):
            raise ValueError("Ya existe un cliente con esa identificación")

        cliente = Cliente(
            nombre=nombre.strip(),
            tipo_identificacion=tipo_identificacion.strip().upper(),
            identificacion=identificacion.strip(),
            email=email.lower().strip() if email else None,
            telefono=telefono.strip() if telefono else None,
            direccion=direccion.strip() if direccion else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def obtener_cliente(self, cliente_id: UUID) -> Optional[Cliente]:
        """Obtiene un cliente por su UUID."""
        return self.db.get(Cliente, cliente_id)

    def obtener_cliente_por_identificacion(
        self, identificacion: str
    ) -> Optional[Cliente]:
        """Obtiene un cliente activo por su número de identificación."""
        return (
            self.db.query(Cliente)
            .filter(
                Cliente.identificacion == (identificacion or "").strip(),
                Cliente.estado,
            )
            .first()
        )

    def obtener_clientes(
        self, skip: int = 0, limit: int = 100, solo_activos: bool = True
    ) -> List[Cliente]:
        """
        Lista clientes con paginación.

        Args:
            skip: Registros a omitir.
            limit: Límite de resultados.
            solo_activos: Si True, retorna solo clientes con estado=True.
        """
        query = self.db.query(Cliente)
        if solo_activos:
            query = query.filter(Cliente.estado)
        return query.offset(skip).limit(limit).all()

    def actualizar_cliente(
        self, cliente_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Cliente]:
        """
        Actualiza los datos de un cliente.
        Campos soportados: nombre, tipo_identificacion, identificacion, email, telefono, direccion, estado.

        Args:
            cliente_id: UUID del cliente.
            id_usuario_edicion: UUID del usuario que edita (opcional).
            **kwargs: Campos a actualizar.

        Returns:
            Instancia actualizada o None si no existe.

        Raises:
            ValueError: Si los datos son inválidos.
        """
        cliente = self.obtener_cliente(cliente_id)
        if not cliente:
            return None

        if "email" in kwargs and kwargs["email"] is not None:
            if not self._validar_email(kwargs["email"]):
                raise ValueError("El formato del email es inválido")
            kwargs["email"] = kwargs["email"].lower().strip()

        if "identificacion" in kwargs and kwargs["identificacion"] is not None:
            nueva_id = kwargs["identificacion"]
            if not self._validar_identificacion(nueva_id):
                raise ValueError("La identificación debe tener al menos 5 caracteres")
            existente = self.obtener_cliente_por_identificacion(nueva_id)
            if existente and existente.id != cliente_id:
                raise ValueError("Ya existe un cliente con esa identificación")
            kwargs["identificacion"] = nueva_id.strip()

        if id_usuario_edicion:
            kwargs["id_usuario_edicion"] = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(cliente, key):
                setattr(cliente, key, value)

        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def eliminar_cliente(
        self, cliente_id: UUID, id_usuario_edicion: Optional[UUID] = None
    ) -> bool:
        """
        Desactiva un cliente (soft delete).

        Args:
            cliente_id: UUID del cliente.
            id_usuario_edicion: UUID del usuario que realiza la acción.

        Returns:
            True si se desactivó, False si no existe.
        """
        cliente = self.obtener_cliente(cliente_id)
        if not cliente:
            return False
        cliente.estado = False
        if id_usuario_edicion:
            cliente.id_usuario_edicion = id_usuario_edicion
        self.db.commit()
        return True
