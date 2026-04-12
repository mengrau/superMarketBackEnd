"""
Esquemas Pydantic (modelos de entrada/salida) para todas las entidades del sistema.
Cada entidad expone tres variantes: Base, Create/Update y Read.
"""

from __future__ import annotations
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timezone
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


def now_utc() -> datetime:
    """Ejecuta now utc."""
    return datetime.now(timezone.utc)


class AuditBase(BaseModel):
    """Campos de auditoría comunes a los esquemas de lectura."""

    fecha_creacion: Optional[datetime] = Field(default_factory=now_utc)
    fecha_actualizacion: Optional[datetime] = Field(default_factory=now_utc)
    id_usuario_creacion: Optional[UUID] = None
    id_usuario_edicion: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)


class UsuarioBase(BaseModel):
    """Campos base del Usuario."""

    username: str = Field(..., max_length=50)
    id_rol: UUID
    estado: Optional[bool] = True


class UsuarioCreate(UsuarioBase):
    """Define la clase UsuarioCreate."""

    password: str = Field(..., min_length=6)


class UsuarioUpdate(BaseModel):
    """Define la clase UsuarioUpdate."""

    username: Optional[str]
    password: Optional[str]
    id_rol: Optional[UUID]
    estado: Optional[bool]


class UsuarioRead(UsuarioBase, AuditBase):
    """Define la clase UsuarioRead."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    """Define la clase LoginRequest."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Define la clase TokenResponse."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class ClienteBase(BaseModel):
    """Campos base del Cliente."""

    nombre: str = Field(..., max_length=120)
    tipo_identificacion: str = Field(..., max_length=5)
    identificacion: str = Field(..., max_length=50)
    email: Optional[str] = Field(None, max_length=120)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    estado: Optional[bool] = True


class ClienteCreate(ClienteBase):
    """Define la clase ClienteCreate."""

    id_usuario_creacion: Optional[UUID] = None


class ClienteUpdate(BaseModel):
    """Define la clase ClienteUpdate."""

    nombre: Optional[str] = Field(None, max_length=120)
    tipo_identificacion: Optional[str] = Field(None, max_length=5)
    identificacion: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=120)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    estado: Optional[bool] = None
    id_usuario_edicion: Optional[UUID] = None


class ClienteRead(ClienteBase, AuditBase):
    """Define la clase ClienteRead."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class EmpleadoBase(BaseModel):
    """Campos base del Empleado."""

    nombre: str = Field(..., max_length=120)
    tipo_identificacion: str = Field(..., max_length=5)
    identificacion: str = Field(..., max_length=50)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    cargo: Optional[str] = Field(None, max_length=80)
    salario: Optional[str] = Field(None, max_length=50)


class EmpleadoCreate(EmpleadoBase):
    """Define la clase EmpleadoCreate."""

    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=6)
    id_rol: UUID
    estado: Optional[bool] = True
    id_usuario_creacion: Optional[UUID] = None


class EmpleadoUpdate(BaseModel):
    """Define la clase EmpleadoUpdate."""

    username: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = Field(None, min_length=6)
    id_rol: Optional[UUID] = None
    estado: Optional[bool] = None
    nombre: Optional[str] = Field(None, max_length=120)
    tipo_identificacion: Optional[str] = Field(None, max_length=5)
    identificacion: Optional[str] = Field(None, max_length=50)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    cargo: Optional[str] = Field(None, max_length=80)
    salario: Optional[str] = Field(None, max_length=50)


class EmpleadoRead(EmpleadoBase, UsuarioRead):
    """Define la clase EmpleadoRead."""

    model_config = ConfigDict(from_attributes=True)


class SucursalBase(BaseModel):
    """Campos base de la Sucursal."""

    nombre: str = Field(..., max_length=120)
    direccion: Optional[str] = Field(None, max_length=200)
    gerente: Optional[str] = Field(None, max_length=120)
    telefono: Optional[str] = Field(None, max_length=20)
    estado: Optional[bool] = True


class SucursalCreate(SucursalBase):
    """Define la clase SucursalCreate."""

    pass


class SucursalUpdate(BaseModel):
    """Define la clase SucursalUpdate."""

    nombre: Optional[str]
    direccion: Optional[str]
    gerente: Optional[str]
    telefono: Optional[str]
    estado: Optional[bool]


class SucursalRead(SucursalBase, AuditBase):
    """Define la clase SucursalRead."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ProveedorBase(BaseModel):
    """Campos base del Proveedor."""

    nombre: str = Field(..., max_length=150)
    nit: str = Field(..., max_length=50)
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    correo: Optional[str] = Field(None, max_length=120)
    estado: Optional[bool] = True


class ProveedorCreate(ProveedorBase):
    """Define la clase ProveedorCreate."""

    pass


class ProveedorUpdate(BaseModel):
    """Define la clase ProveedorUpdate."""

    nombre: Optional[str]
    nit: Optional[str]
    telefono: Optional[str]
    direccion: Optional[str]
    correo: Optional[str]
    estado: Optional[bool]


class ProveedorRead(ProveedorBase, AuditBase):
    """Define la clase ProveedorRead."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TipoProductoBase(BaseModel):
    """Campos base del TipoProducto."""

    nombre: str = Field(..., max_length=120)
    descripcion: Optional[str] = Field(None, max_length=300)
    estado: Optional[bool] = True


class TipoProductoCreate(TipoProductoBase):
    """Define la clase TipoProductoCreate."""

    pass


class TipoProductoUpdate(BaseModel):
    """Define la clase TipoProductoUpdate."""

    nombre: Optional[str]
    descripcion: Optional[str]
    estado: Optional[bool]


class TipoProductoRead(TipoProductoBase):
    """Define la clase TipoProductoRead."""

    id: UUID
    fecha_creacion: Optional[datetime] = Field(default_factory=now_utc)
    fecha_actualizacion: Optional[datetime] = Field(default_factory=now_utc)

    model_config = ConfigDict(from_attributes=True)


class ProductoBase(BaseModel):
    """Campos base del Producto."""

    nombre: str = Field(..., max_length=200)
    codigo_barras: Optional[str] = Field(None, max_length=100)
    precio_venta: Decimal = Field(..., gt=0)
    fecha_vencimiento: Optional[datetime] = None
    id_tipo: Optional[UUID] = None
    id_proveedor: Optional[UUID] = None
    estado: Optional[bool] = True


class ProductoCreate(ProductoBase):
    """Define la clase ProductoCreate."""

    pass


class ProductoUpdate(BaseModel):
    """Define la clase ProductoUpdate."""

    nombre: Optional[str]
    codigo_barras: Optional[str]
    precio_venta: Optional[Decimal]
    fecha_vencimiento: Optional[datetime]
    id_tipo: Optional[UUID]
    id_proveedor: Optional[UUID]
    estado: Optional[bool]


class ProductoRead(ProductoBase, AuditBase):
    """Define la clase ProductoRead."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class InventarioBase(BaseModel):
    """Campos base del Inventario."""

    stock_actual: int = Field(..., ge=0)
    stock_minimo: int = Field(..., ge=0)
    ubicacion: Optional[str] = Field(None, max_length=200)
    id_producto: UUID
    id_sucursal: UUID
    estado: Optional[bool] = True


class InventarioCreate(InventarioBase):
    """Define la clase InventarioCreate."""

    pass


class InventarioUpdate(BaseModel):
    """Define la clase InventarioUpdate."""

    stock_actual: Optional[int]
    stock_minimo: Optional[int]
    ubicacion: Optional[str]
    id_producto: Optional[UUID]
    id_sucursal: Optional[UUID]
    estado: Optional[bool]


class InventarioRead(InventarioBase, AuditBase):
    """Define la clase InventarioRead."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class DetalleFacturaBase(BaseModel):
    """Campos base del DetalleFactura."""

    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., gt=0)
    subtotal: Decimal = Field(..., gt=0)
    id_factura: UUID
    id_producto: UUID


class DetalleFacturaCreate(BaseModel):
    """Define la clase DetalleFacturaCreate."""

    cantidad: int = Field(..., gt=0)
    precio_unitario: Decimal = Field(..., gt=0)
    id_producto: UUID


class DetalleFacturaUpdate(BaseModel):
    """Define la clase DetalleFacturaUpdate."""

    cantidad: Optional[int]
    precio_unitario: Optional[Decimal]


class DetalleFacturaRead(DetalleFacturaBase):
    """Define la clase DetalleFacturaRead."""

    id: UUID
    fecha_creacion: Optional[datetime] = Field(default_factory=now_utc)

    model_config = ConfigDict(from_attributes=True)


class FacturaBase(BaseModel):
    """Campos base de la Factura."""

    fecha: Optional[datetime] = Field(default_factory=now_utc)
    total: Decimal = Field(..., ge=0)
    metodo_pago: Optional[str] = Field(None, max_length=80)
    id_cliente: UUID
    id_empleado: UUID
    id_sucursal: UUID
    estado: Optional[str] = Field(default="emitida", max_length=30)


class FacturaCreate(BaseModel):
    """Define la clase FacturaCreate."""

    metodo_pago: Optional[str]
    id_cliente: UUID
    id_empleado: UUID
    id_sucursal: UUID
    detalles: List[DetalleFacturaCreate] = Field(default_factory=list)


class FacturaUpdate(BaseModel):
    """Define la clase FacturaUpdate."""

    metodo_pago: Optional[str]
    estado: Optional[str]


class FacturaRead(FacturaBase, AuditBase):
    """Define la clase FacturaRead."""

    id: UUID
    detalles: List[DetalleFacturaRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class DetalleCompraBase(BaseModel):
    """Campos base del DetalleCompra."""

    cantidad: int = Field(..., gt=0)
    precio_compra: Decimal = Field(..., gt=0)
    id_compra: UUID
    id_producto: UUID


class DetalleCompraCreate(BaseModel):
    """Define la clase DetalleCompraCreate."""

    cantidad: int = Field(..., gt=0)
    precio_compra: Decimal = Field(..., gt=0)
    id_producto: UUID


class DetalleCompraUpdate(BaseModel):
    """Define la clase DetalleCompraUpdate."""

    cantidad: Optional[int]
    precio_compra: Optional[Decimal]


class DetalleCompraRead(DetalleCompraBase):
    """Define la clase DetalleCompraRead."""

    id: UUID
    fecha_creacion: Optional[datetime] = Field(default_factory=now_utc)

    model_config = ConfigDict(from_attributes=True)


class CompraProveedorBase(BaseModel):
    """Campos base de la CompraProveedor."""

    fecha: Optional[datetime] = Field(default_factory=now_utc)
    total_compra: Decimal = Field(..., ge=0)
    id_proveedor: UUID
    id_sucursal: Optional[UUID] = None
    estado: Optional[str] = Field(default="recibida", max_length=30)


class CompraProveedorCreate(BaseModel):
    """Define la clase CompraProveedorCreate."""

    id_proveedor: UUID
    id_sucursal: Optional[UUID] = None
    detalles: List[DetalleCompraCreate] = Field(default_factory=list)


class CompraProveedorUpdate(BaseModel):
    """Define la clase CompraProveedorUpdate."""

    estado: Optional[str]


class CompraProveedorRead(CompraProveedorBase, AuditBase):
    """Define la clase CompraProveedorRead."""

    id: UUID
    detalles: List[DetalleCompraRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class RolBase(BaseModel):
    """Campos base del Rol."""

    nombre: str = Field(..., max_length=80)
    descripcion: Optional[str] = Field(None, max_length=250)
    salario: Optional[Decimal] = None
    activo: Optional[bool] = True


class RolCreate(RolBase):
    """Define la clase RolCreate."""

    pass


class RolUpdate(BaseModel):
    """Define la clase RolUpdate."""

    nombre: Optional[str]
    descripcion: Optional[str]
    salario: Optional[Decimal]
    activo: Optional[bool]


class RolRead(RolBase):
    """Define la clase RolRead."""

    id: UUID
    fecha_creacion: Optional[datetime] = Field(default_factory=now_utc)
    fecha_actualizacion: Optional[datetime] = Field(default_factory=now_utc)

    model_config = ConfigDict(from_attributes=True)
