"""Seeders idempotentes para datos iniciales del proyecto SuperMarket.

El flujo replica el enfoque usado en clase-aplicacion-web:
1. Crear/obtener usuario administrador.
2. Sembrar catálogos y maestros en orden.
3. Evitar duplicados usando claves de negocio.
"""

import uuid
from collections.abc import Iterable
from decimal import Decimal
from typing import Any

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.auth import hash_password, verify_password
from core.config import SessionLocal
from entities.cliente import Cliente
from entities.empleado import Empleado
from entities.producto import Producto
from entities.proveedor import Proveedor
from entities.rol import Rol
from entities.sucursal import Sucursal
from entities.tipoProducto import TipoProducto
from entities.usuario import Usuario

ROLE_SEED_DATA: list[dict[str, Any]] = [
    {
        "nombre": "admin",
        "descripcion": "Usuario administrador con acceso total",
        "salario": Decimal("3000"),
        "aliases": ["Administrador"],
    },
    {
        "nombre": "gerente",
        "descripcion": "Gerente de sucursal",
        "salario": Decimal("2500"),
        "aliases": ["Gerente"],
    },
    {
        "nombre": "empleado",
        "descripcion": "Empleado de caja y atención",
        "salario": Decimal("1200"),
        "aliases": ["Empleado"],
    },
]

SUCURSALES_SEED_DATA: list[dict[str, str]] = [
    {
        "nombre": "SuperMarket Centro",
        "direccion": "Calle Principal 123",
        "gerente": "Juan García",
        "telefono": "(555) 123-4567",
    },
    {
        "nombre": "SuperMarket Norte",
        "direccion": "Avenida Norte 456",
        "gerente": "María López",
        "telefono": "(555) 234-5678",
    },
    {
        "nombre": "SuperMarket Sur",
        "direccion": "Carrera Sur 789",
        "gerente": "Carlos Rodríguez",
        "telefono": "(555) 345-6789",
    },
]

TIPOS_PRODUCTO_SEED_DATA: list[dict[str, str]] = [
    {"nombre": "Alimentos", "descripcion": "Productos alimenticios en general"},
    {"nombre": "Bebidas", "descripcion": "Bebidas alcohólicas y no alcohólicas"},
    {"nombre": "Lácteos", "descripcion": "Productos lácteos y derivados"},
    {
        "nombre": "Carnes y Pescados",
        "descripcion": "Carnes frescas, aves y pescados",
    },
    {"nombre": "Frutas y Verduras", "descripcion": "Productos frescos"},
    {
        "nombre": "Productos de Limpieza",
        "descripcion": "Artículos de limpieza del hogar",
    },
    {
        "nombre": "Higiene Personal",
        "descripcion": "Productos de higiene y cuidado personal",
    },
    {"nombre": "Productos Congelados", "descripcion": "Alimentos congelados"},
]

PROVEEDORES_SEED_DATA: list[dict[str, str]] = [
    {
        "nombre": "Distribuidora Nacional",
        "nit": "800123456789",
        "telefono": "(555) 111-2222",
        "correo": "contacto@distribuidora.com",
        "direccion": "Calle Industrial 100",
    },
    {
        "nombre": "Importaciones Rápidas",
        "nit": "800234567890",
        "telefono": "(555) 222-3333",
        "correo": "info@importaciones.com",
        "direccion": "Avenida Comercial 200",
    },
    {
        "nombre": "Productos Frescos SA",
        "nit": "800345678901",
        "telefono": "(555) 333-4444",
        "correo": "ventas@frescos.com",
        "direccion": "Zona Agrícola 300",
    },
]

PRODUCTOS_SEED_DATA: list[dict[str, Any]] = [
    {
        "nombre": "Leche Entera 1L",
        "tipo_idx": 2,
        "proveedor_idx": 0,
        "precio": Decimal("2.50"),
        "codigo_barras": "7501234567890",
    },
    {
        "nombre": "Pan Integral",
        "tipo_idx": 0,
        "proveedor_idx": 0,
        "precio": Decimal("1.50"),
        "codigo_barras": "7501234567891",
    },
    {
        "nombre": "Queso Cheddar 200g",
        "tipo_idx": 2,
        "proveedor_idx": 0,
        "precio": Decimal("4.99"),
        "codigo_barras": "7501234567892",
    },
    {
        "nombre": "Yogurt Natural 125g",
        "tipo_idx": 2,
        "proveedor_idx": 0,
        "precio": Decimal("1.20"),
        "codigo_barras": "7501234567893",
    },
    {
        "nombre": "Pollo Fresco kg",
        "tipo_idx": 3,
        "proveedor_idx": 2,
        "precio": Decimal("8.50"),
        "codigo_barras": "7501234567894",
    },
    {
        "nombre": "Atún en Lata",
        "tipo_idx": 3,
        "proveedor_idx": 2,
        "precio": Decimal("2.80"),
        "codigo_barras": "7501234567895",
    },
    {
        "nombre": "Manzanas kg",
        "tipo_idx": 4,
        "proveedor_idx": 2,
        "precio": Decimal("3.00"),
        "codigo_barras": "7501234567896",
    },
    {
        "nombre": "Lechuga Fresca",
        "tipo_idx": 4,
        "proveedor_idx": 2,
        "precio": Decimal("1.75"),
        "codigo_barras": "7501234567897",
    },
    {
        "nombre": "Detergente Líquido",
        "tipo_idx": 5,
        "proveedor_idx": 1,
        "precio": Decimal("3.99"),
        "codigo_barras": "7501234567898",
    },
    {
        "nombre": "Jabón de Manos",
        "tipo_idx": 6,
        "proveedor_idx": 1,
        "precio": Decimal("2.50"),
        "codigo_barras": "7501234567899",
    },
    {
        "nombre": "Agua Embotellada 6 pack",
        "tipo_idx": 1,
        "proveedor_idx": 1,
        "precio": Decimal("1.99"),
        "codigo_barras": "7501234567800",
    },
    {
        "nombre": "Refresco Gaseoso",
        "tipo_idx": 1,
        "proveedor_idx": 1,
        "precio": Decimal("2.20"),
        "codigo_barras": "7501234567801",
    },
]

CLIENTES_SEED_DATA: list[dict[str, str]] = [
    {
        "nombre": "Juan Carlos García",
        "tipo_identificacion": "CC",
        "identificacion": "1234567890",
        "email": "juan.garcia@email.com",
        "telefono": "(555) 100-0001",
        "direccion": "Calle Falsa 123",
    },
    {
        "nombre": "María Elena López",
        "tipo_identificacion": "CC",
        "identificacion": "0987654321",
        "email": "maria.lopez@email.com",
        "telefono": "(555) 100-0002",
        "direccion": "Avenida Principal 456",
    },
    {
        "nombre": "Roberto Díaz Martín",
        "tipo_identificacion": "CE",
        "identificacion": "1122334455",
        "email": "roberto.diaz@email.com",
        "telefono": "(555) 100-0003",
        "direccion": "Carrera Central 789",
    },
    {
        "nombre": "Ana Rodríguez Pérez",
        "tipo_identificacion": "PA",
        "identificacion": "9876543210",
        "email": "ana.rodriguez@email.com",
        "telefono": "(555) 100-0004",
        "direccion": "Paseo Comercial 321",
    },
]

EMPLEADOS_SEED_DATA: list[dict[str, str]] = [
    {
        "nombre": "Carlos Mendoza",
        "username": "carlos.mendoza",
        "tipo_identificacion": "CC",
        "identificacion": "1111111111",
        "telefono": "(555) 201-0001",
        "direccion": "Calle 1 #100",
        "cargo": "Cajero",
        "rol": "empleado",
    },
    {
        "nombre": "Diana Torres",
        "username": "diana.torres",
        "tipo_identificacion": "CC",
        "identificacion": "2222222222",
        "telefono": "(555) 201-0002",
        "direccion": "Calle 2 #200",
        "cargo": "Reponedor",
        "rol": "empleado",
    },
    {
        "nombre": "Felipe Ramírez",
        "username": "felipe.ramirez",
        "tipo_identificacion": "CC",
        "identificacion": "3333333333",
        "telefono": "(555) 201-0003",
        "direccion": "Calle 3 #300",
        "cargo": "Gerente de Turno",
        "rol": "gerente",
    },
]


def _find_role_by_aliases(db: Session, name: str, aliases: Iterable[str]) -> Rol | None:
    """Buscar rol por nombre canónico o alias, ignorando mayúsculas/minúsculas."""
    candidates = [name, *aliases]
    normalized = [candidate.strip().lower() for candidate in candidates if candidate]
    return db.query(Rol).filter(func.lower(Rol.nombre).in_(normalized)).first()


def seed_roles(db: Session) -> dict[str, Rol]:
    """Sembrar roles base y devolverlos indexados por nombre canónico."""
    roles: dict[str, Rol] = {}
    for item in ROLE_SEED_DATA:
        role = _find_role_by_aliases(db, item["nombre"], item.get("aliases", []))
        if role:
            print(f"  ✓ Rol '{item['nombre']}' ya existe")
            roles[item["nombre"]] = role
            continue

        role = Rol(
            id=uuid.uuid4(),
            nombre=item["nombre"],
            descripcion=item["descripcion"],
            salario=item["salario"],
            activo=True,
        )
        db.add(role)
        db.flush()
        print(f"  ✓ Rol '{item['nombre']}' creado")
        roles[item["nombre"]] = role

    db.commit()
    return roles


def get_or_create_admin(db: Session, admin_role: Rol) -> Usuario:
    """Crear el usuario administrador si no existe y devolver su instancia."""
    admin = db.query(Usuario).filter(Usuario.username == "admin").first()
    if admin:
        needs_update = False
        if not admin.estado:
            admin.estado = True
            needs_update = True
        if admin.id_rol != admin_role.id:
            admin.id_rol = admin_role.id
            needs_update = True
        if not verify_password("admin123", admin.password_hash):
            admin.password_hash = hash_password("admin123")
            needs_update = True
        if needs_update:
            db.commit()
            db.refresh(admin)
            print("  ✓ Usuario 'admin' actualizado")
        else:
            print("  ✓ Usuario 'admin' ya existe")
        return admin

    admin = Usuario(
        id=uuid.uuid4(),
        username="admin",
        password_hash=hash_password("admin123"),
        id_rol=admin_role.id,
        rol=admin_role,
        estado=True,
        tipo="usuario",
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("  ✓ Usuario 'admin' creado (contraseña: admin123)")
    return admin


def _seed_sucursales(db: Session, created_by: Usuario) -> list[Sucursal]:
    """Sembrar sucursales base de forma idempotente."""
    records: list[Sucursal] = []
    for item in SUCURSALES_SEED_DATA:
        existing = db.query(Sucursal).filter(Sucursal.nombre == item["nombre"]).first()
        if existing:
            print(f"  ✓ Sucursal '{item['nombre']}' ya existe")
            records.append(existing)
            continue

        record = Sucursal(
            id=uuid.uuid4(),
            nombre=item["nombre"],
            direccion=item["direccion"],
            gerente=item["gerente"],
            telefono=item["telefono"],
            estado=True,
            id_usuario_creacion=created_by.id,
        )
        db.add(record)
        db.flush()
        print(f"  ✓ Sucursal '{item['nombre']}' creada")
        records.append(record)

    db.commit()
    return records


def _seed_tipos_producto(db: Session) -> list[TipoProducto]:
    """Sembrar catálogo de tipos de producto de forma idempotente."""
    records: list[TipoProducto] = []
    for item in TIPOS_PRODUCTO_SEED_DATA:
        existing = (
            db.query(TipoProducto).filter(TipoProducto.nombre == item["nombre"]).first()
        )
        if existing:
            print(f"  ✓ Tipo de producto '{item['nombre']}' ya existe")
            records.append(existing)
            continue

        record = TipoProducto(
            id=uuid.uuid4(),
            nombre=item["nombre"],
            descripcion=item["descripcion"],
            estado=True,
        )
        db.add(record)
        db.flush()
        print(f"  ✓ Tipo de producto '{item['nombre']}' creado")
        records.append(record)

    db.commit()
    return records


def _seed_proveedores(db: Session, created_by: Usuario) -> list[Proveedor]:
    """Sembrar proveedores base de forma idempotente."""
    records: list[Proveedor] = []
    for item in PROVEEDORES_SEED_DATA:
        existing = db.query(Proveedor).filter(Proveedor.nit == item["nit"]).first()
        if existing:
            print(f"  ✓ Proveedor '{item['nombre']}' ya existe")
            records.append(existing)
            continue

        record = Proveedor(
            id=uuid.uuid4(),
            nombre=item["nombre"],
            nit=item["nit"],
            telefono=item["telefono"],
            correo=item["correo"],
            direccion=item["direccion"],
            estado=True,
            id_usuario_creacion=created_by.id,
        )
        db.add(record)
        db.flush()
        print(f"  ✓ Proveedor '{item['nombre']}' creado")
        records.append(record)

    db.commit()
    return records


def _seed_productos(
    db: Session,
    tipos_producto: list[TipoProducto],
    proveedores: list[Proveedor],
    created_by: Usuario,
) -> list[Producto]:
    """Sembrar productos base de forma idempotente."""
    records: list[Producto] = []
    for item in PRODUCTOS_SEED_DATA:
        existing = (
            db.query(Producto)
            .filter(Producto.codigo_barras == item["codigo_barras"])
            .first()
        )
        if existing:
            print(f"  ✓ Producto '{item['nombre']}' ya existe")
            records.append(existing)
            continue

        record = Producto(
            id=uuid.uuid4(),
            nombre=item["nombre"],
            id_tipo=tipos_producto[item["tipo_idx"]].id,
            id_proveedor=proveedores[item["proveedor_idx"]].id,
            precio_venta=item["precio"],
            codigo_barras=item["codigo_barras"],
            estado=True,
            id_usuario_creacion=created_by.id,
        )
        db.add(record)
        db.flush()
        print(f"  ✓ Producto '{item['nombre']}' creado")
        records.append(record)

    db.commit()
    return records


def _seed_clientes(db: Session, created_by: Usuario) -> list[Cliente]:
    """Sembrar clientes base de forma idempotente."""
    records: list[Cliente] = []
    for item in CLIENTES_SEED_DATA:
        existing = (
            db.query(Cliente)
            .filter(Cliente.identificacion == item["identificacion"])
            .first()
        )
        if existing:
            print(f"  ✓ Cliente '{item['nombre']}' ya existe")
            records.append(existing)
            continue

        record = Cliente(
            id=uuid.uuid4(),
            nombre=item["nombre"],
            tipo_identificacion=item["tipo_identificacion"],
            identificacion=item["identificacion"],
            email=item["email"],
            telefono=item["telefono"],
            direccion=item["direccion"],
            estado=True,
            id_usuario_creacion=created_by.id,
        )
        db.add(record)
        db.flush()
        print(f"  ✓ Cliente '{item['nombre']}' creado")
        records.append(record)

    db.commit()
    return records


def _seed_empleados(
    db: Session,
    role_by_name: dict[str, Rol],
    created_by: Usuario,
) -> list[Empleado]:
    """Sembrar empleados base de forma idempotente."""
    records: list[Empleado] = []
    for item in EMPLEADOS_SEED_DATA:
        existing = (
            db.query(Empleado).filter(Empleado.username == item["username"]).first()
        )
        if existing:
            print(f"  ✓ Empleado '{item['nombre']}' ya existe")
            records.append(existing)
            continue

        role_name = "gerente" if item["rol"] == "gerente" else "empleado"
        role = role_by_name[role_name]

        record = Empleado(
            id=uuid.uuid4(),
            username=item["username"],
            password_hash=hash_password("empleado123"),
            id_rol=role.id,
            rol=role,
            estado=True,
            tipo="empleado",
            nombre=item["nombre"],
            tipo_identificacion=item["tipo_identificacion"],
            identificacion=item["identificacion"],
            telefono=item["telefono"],
            direccion=item["direccion"],
            cargo=item["cargo"],
            id_usuario_creacion=created_by.id,
        )
        db.add(record)
        db.flush()
        print(f"  ✓ Empleado '{item['nombre']}' creado (usuario: {item['username']})")
        records.append(record)

    db.commit()
    return records


def seed_database() -> None:
    """Sembrar datos iniciales con flujo idempotente y transaccional."""
    print("\n" + "=" * 60)
    print("INICIANDO SEEDERS DE BASE DE DATOS")
    print("=" * 60 + "\n")

    db = SessionLocal()
    try:
        print("1. Creando Roles...")
        roles = seed_roles(db)
        print()

        print("2. Creando Usuario Administrador...")
        admin = get_or_create_admin(db, roles["admin"])
        print()

        print("3. Creando Sucursales...")
        sucursales = _seed_sucursales(db, admin)
        print()

        print("4. Creando Tipos de Productos...")
        tipos_producto = _seed_tipos_producto(db)
        print()

        print("5. Creando Proveedores...")
        proveedores = _seed_proveedores(db, admin)
        print()

        print("6. Creando Productos...")
        productos = _seed_productos(db, tipos_producto, proveedores, admin)
        print()

        print("7. Creando Clientes...")
        clientes = _seed_clientes(db, admin)
        print()

        print("8. Creando Empleados...")
        empleados = _seed_empleados(db, roles, admin)
        print()

        print("=" * 60)
        print("SEEDERS COMPLETADOS EXITOSAMENTE")
        print("=" * 60)
        print("\nResumen:")
        print(f"  - Roles: {len(roles)}")
        print(f"  - Usuarios: {len(empleados) + 1} (admin + empleados)")
        print(f"  - Sucursales: {len(sucursales)}")
        print(f"  - Tipos de Producto: {len(tipos_producto)}")
        print(f"  - Productos: {len(productos)}")
        print(f"  - Proveedores: {len(proveedores)}")
        print(f"  - Clientes: {len(clientes)}")
        print(f"  - Empleados: {len(empleados)}")
        print("\nCredenciales por defecto:")
        print("  - Usuario admin: admin / admin123")
        print("  - Empleados: {username} / empleado123")
        print()
    except IntegrityError:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def main() -> None:
    """Punto de entrada para ejecución manual del seeder."""
    seed_database()


if __name__ == "__main__":
    main()
