"""
Script de seeders para popular la base de datos con datos de prueba.
Ejecutar: python -m src.database.seeders
"""

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.config import SessionLocal, engine, Base
from auth.security import hash_password
from entities.rol import Rol
from entities.usuario import Usuario
from entities.sucursal import Sucursal
from entities.tipoProducto import TipoProducto
from entities.producto import Producto
from entities.proveedor import Proveedor
from entities.cliente import Cliente
from entities.empleado import Empleado


def crear_rol(db: Session, nombre: str, descripcion: str, salario: Decimal = None) -> Rol:
    """Crear un rol si no existe."""
    rol_existente = db.query(Rol).filter(Rol.nombre == nombre).first()
    if rol_existente:
        print(f"  ✓ Rol '{nombre}' ya existe")
        return rol_existente

    rol = Rol(
        id=uuid.uuid4(),
        nombre=nombre,
        descripcion=descripcion,
        salario=salario,
        activo=True,
    )
    db.add(rol)
    db.commit()
    db.refresh(rol)
    print(f"  ✓ Rol '{nombre}' creado")
    return rol


def crear_usuario_admin(db: Session, rol_admin: Rol) -> Usuario:
    """Crear usuario administrador si no existe."""
    usuario_existente = db.query(Usuario).filter(
        Usuario.username == "admin"
    ).first()
    if usuario_existente:
        print(f"  ✓ Usuario 'admin' ya existe")
        return usuario_existente

    usuario = Usuario(
        id=uuid.uuid4(),
        username="admin",
        password_hash=hash_password("admin123"),
        id_rol=rol_admin.id,
        rol=rol_admin,
        estado=True,
        tipo="usuario",
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    print(f"  ✓ Usuario 'admin' creado (contraseña: admin123)")
    return usuario


def crear_sucursales(db: Session, usuario_admin: Usuario) -> list:
    """Crear sucursales de prueba."""
    sucursales_data = [
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

    sucursales = []
    for data in sucursales_data:
        sucursal_existente = db.query(Sucursal).filter(
            Sucursal.nombre == data["nombre"]
        ).first()
        if sucursal_existente:
            print(f"  ✓ Sucursal '{data['nombre']}' ya existe")
            sucursales.append(sucursal_existente)
            continue

        sucursal = Sucursal(
            id=uuid.uuid4(),
            nombre=data["nombre"],
            direccion=data["direccion"],
            gerente=data["gerente"],
            telefono=data["telefono"],
            estado=True,
            id_usuario_creacion=usuario_admin.id,
        )
        db.add(sucursal)
        db.commit()
        db.refresh(sucursal)
        print(f"  ✓ Sucursal '{data['nombre']}' creada")
        sucursales.append(sucursal)

    return sucursales


def crear_tipos_producto(db: Session) -> list:
    """Crear tipos de productos."""
    tipos_data = [
        {"nombre": "Alimentos", "descripcion": "Productos alimenticios en general"},
        {"nombre": "Bebidas", "descripcion": "Bebidas alcohólicas y no alcohólicas"},
        {
            "nombre": "Lácteos",
            "descripcion": "Productos lácteos y derivados",
        },
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

    tipos = []
    for data in tipos_data:
        tipo_existente = db.query(TipoProducto).filter(
            TipoProducto.nombre == data["nombre"]
        ).first()
        if tipo_existente:
            print(f"  ✓ Tipo de producto '{data['nombre']}' ya existe")
            tipos.append(tipo_existente)
            continue

        tipo = TipoProducto(
            id=uuid.uuid4(),
            nombre=data["nombre"],
            descripcion=data["descripcion"],
            estado=True,
        )
        db.add(tipo)
        db.commit()
        db.refresh(tipo)
        print(f"  ✓ Tipo de producto '{data['nombre']}' creado")
        tipos.append(tipo)

    return tipos


def crear_proveedores(db: Session, usuario_admin: Usuario) -> list:
    """Crear proveedores de prueba."""
    proveedores_data = [
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

    proveedores = []
    for data in proveedores_data:
        proveedor_existente = db.query(Proveedor).filter(
            Proveedor.nombre == data["nombre"]
        ).first()
        if proveedor_existente:
            print(f"  ✓ Proveedor '{data['nombre']}' ya existe")
            proveedores.append(proveedor_existente)
            continue

        proveedor = Proveedor(
            id=uuid.uuid4(),
            nombre=data["nombre"],
            nit=data["nit"],
            telefono=data["telefono"],
            correo=data["correo"],
            direccion=data["direccion"],
            estado=True,
            id_usuario_creacion=usuario_admin.id,
        )
        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)
        print(f"  ✓ Proveedor '{data['nombre']}' creado")
        proveedores.append(proveedor)

    return proveedores


def crear_productos(
    db: Session, tipos: list, proveedores: list, usuario_admin: Usuario
) -> list:
    """Crear productos de prueba."""
    productos_data = [
        {
            "nombre": "Leche Entera 1L",
            "tipo_idx": 2,  # Lácteos
            "proveedor_idx": 0,
            "precio": Decimal("2.50"),
            "codigo_barras": "7501234567890",
        },
        {
            "nombre": "Pan Integral",
            "tipo_idx": 0,  # Alimentos
            "proveedor_idx": 0,
            "precio": Decimal("1.50"),
            "codigo_barras": "7501234567891",
        },
        {
            "nombre": "Queso Cheddar 200g",
            "tipo_idx": 2,  # Lácteos
            "proveedor_idx": 0,
            "precio": Decimal("4.99"),
            "codigo_barras": "7501234567892",
        },
        {
            "nombre": "Yogurt Natural 125g",
            "tipo_idx": 2,  # Lácteos
            "proveedor_idx": 0,
            "precio": Decimal("1.20"),
            "codigo_barras": "7501234567893",
        },
        {
            "nombre": "Pollo Fresco kg",
            "tipo_idx": 3,  # Carnes
            "proveedor_idx": 2,
            "precio": Decimal("8.50"),
            "codigo_barras": "7501234567894",
        },
        {
            "nombre": "Atún en Lata",
            "tipo_idx": 3,  # Carnes y Pescados
            "proveedor_idx": 2,
            "precio": Decimal("2.80"),
            "codigo_barras": "7501234567895",
        },
        {
            "nombre": "Manzanas kg",
            "tipo_idx": 4,  # Frutas y Verduras
            "proveedor_idx": 2,
            "precio": Decimal("3.00"),
            "codigo_barras": "7501234567896",
        },
        {
            "nombre": "Lechuga Fresca",
            "tipo_idx": 4,  # Frutas y Verduras
            "proveedor_idx": 2,
            "precio": Decimal("1.75"),
            "codigo_barras": "7501234567897",
        },
        {
            "nombre": "Detergente Líquido",
            "tipo_idx": 5,  # Limpieza
            "proveedor_idx": 1,
            "precio": Decimal("3.99"),
            "codigo_barras": "7501234567898",
        },
        {
            "nombre": "Jabón de Manos",
            "tipo_idx": 6,  # Higiene
            "proveedor_idx": 1,
            "precio": Decimal("2.50"),
            "codigo_barras": "7501234567899",
        },
        {
            "nombre": "Agua Embotellada 6 pack",
            "tipo_idx": 1,  # Bebidas
            "proveedor_idx": 1,
            "precio": Decimal("1.99"),
            "codigo_barras": "7501234567800",
        },
        {
            "nombre": "Refresco Gaseoso",
            "tipo_idx": 1,  # Bebidas
            "proveedor_idx": 1,
            "precio": Decimal("2.20"),
            "codigo_barras": "7501234567801",
        },
    ]

    productos = []
    for data in productos_data:
        producto_existente = db.query(Producto).filter(
            Producto.nombre == data["nombre"]
        ).first()
        if producto_existente:
            print(f"  ✓ Producto '{data['nombre']}' ya existe")
            productos.append(producto_existente)
            continue

        producto = Producto(
            id=uuid.uuid4(),
            nombre=data["nombre"],
            id_tipo=tipos[data["tipo_idx"]].id,
            tipo=tipos[data["tipo_idx"]],
            id_proveedor=proveedores[data["proveedor_idx"]].id,
            proveedor=proveedores[data["proveedor_idx"]],
            precio_venta=data["precio"],
            codigo_barras=data["codigo_barras"],
            estado=True,
            id_usuario_creacion=usuario_admin.id,
        )
        db.add(producto)
        db.commit()
        db.refresh(producto)
        print(f"  ✓ Producto '{data['nombre']}' creado")
        productos.append(producto)

    return productos


def crear_clientes(db: Session, usuario_admin: Usuario) -> list:
    """Crear clientes de prueba."""
    clientes_data = [
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

    clientes = []
    for data in clientes_data:
        cliente_existente = db.query(Cliente).filter(
            Cliente.email == data["email"]
        ).first()
        if cliente_existente:
            print(f"  ✓ Cliente '{data['nombre']}' ya existe")
            clientes.append(cliente_existente)
            continue

        cliente = Cliente(
            id=uuid.uuid4(),
            nombre=data["nombre"],
            tipo_identificacion=data["tipo_identificacion"],
            identificacion=data["identificacion"],
            email=data["email"],
            telefono=data["telefono"],
            direccion=data["direccion"],
            estado=True,
            id_usuario_creacion=usuario_admin.id,
        )
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        print(f"  ✓ Cliente '{data['nombre']}' creado")
        clientes.append(cliente)

    return clientes


def crear_empleados(
    db: Session, rol_empleado: Rol, rol_gerente: Rol, usuario_admin: Usuario
) -> list:
    """Crear empleados de prueba."""
    empleados_data = [
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

    empleados = []
    for data in empleados_data:
        empleado_existente = db.query(Empleado).filter(
            Empleado.username == data["username"]
        ).first()
        if empleado_existente:
            print(f"  ✓ Empleado '{data['nombre']}' ya existe")
            empleados.append(empleado_existente)
            continue

        rol = rol_gerente if data["rol"] == "gerente" else rol_empleado
        
        empleado = Empleado(
            id=uuid.uuid4(),
            username=data["username"],
            password_hash=hash_password("empleado123"),
            id_rol=rol.id,
            rol=rol,
            estado=True,
            tipo="empleado",
            nombre=data["nombre"],
            tipo_identificacion=data["tipo_identificacion"],
            identificacion=data["identificacion"],
            telefono=data["telefono"],
            direccion=data["direccion"],
            cargo=data["cargo"],
            id_usuario_creacion=usuario_admin.id,
        )
        db.add(empleado)
        db.commit()
        db.refresh(empleado)
        print(f"  ✓ Empleado '{data['nombre']}' creado (usuario: {data['username']})")
        empleados.append(empleado)

    return empleados


def seed_database():
    """Ejecutar todos los seeders."""
    print("\n" + "=" * 60)
    print("INICIANDO SEEDERS DE BASE DE DATOS")
    print("=" * 60 + "\n")

    db = SessionLocal()

    try:
        # 1. Crear roles
        print("1. Creando Roles...")
        rol_admin = crear_rol(
            db,
            "Administrador",
            "Usuario administrador con acceso total",
            Decimal("3000"),
        )
        rol_gerente = crear_rol(
            db, "Gerente", "Gerente de sucursal", Decimal("2500")
        )
        rol_empleado = crear_rol(
            db,
            "Empleado",
            "Empleado de caja y atención",
            Decimal("1200"),
        )
        rol_analista = crear_rol(
            db,
            "Analista",
            "Analista de inventario",
            Decimal("1500"),
        )
        print()

        # 2. Crear usuario administrador
        print("2. Creando Usuario Administrador...")
        usuario_admin = crear_usuario_admin(db, rol_admin)
        print()

        # 3. Crear sucursales
        print("3. Creando Sucursales...")
        sucursales = crear_sucursales(db, usuario_admin)
        print()

        # 4. Crear tipos de productos
        print("4. Creando Tipos de Productos...")
        tipos_producto = crear_tipos_producto(db)
        print()

        # 5. Crear proveedores
        print("5. Creando Proveedores...")
        proveedores = crear_proveedores(db, usuario_admin)
        print()

        # 6. Crear productos
        print("6. Creando Productos...")
        productos = crear_productos(db, tipos_producto, proveedores, usuario_admin)
        print()

        # 7. Crear clientes
        print("7. Creando Clientes...")
        clientes = crear_clientes(db, usuario_admin)
        print()

        # 8. Crear empleados
        print("8. Creando Empleados...")
        empleados = crear_empleados(db, rol_empleado, rol_gerente, usuario_admin)
        print()

        print("=" * 60)
        print("✓ SEEDERS COMPLETADOS EXITOSAMENTE")
        print("=" * 60)
        print("\n📊 Resumen:")
        print(f"  • Roles: 4")
        print(f"  • Usuarios: {len(empleados) + 1} (admin + empleados)")
        print(f"  • Sucursales: {len(sucursales)}")
        print(f"  • Tipos de Producto: {len(tipos_producto)}")
        print(f"  • Productos: {len(productos)}")
        print(f"  • Proveedores: {len(proveedores)}")
        print(f"  • Clientes: {len(clientes)}")
        print(f"  • Empleados: {len(empleados)}")
        print("\n🔑 Credenciales por defecto:")
        print("  • Usuario admin: admin / admin123")
        print("  • Empleados: {username} / empleado123")
        print()

    except IntegrityError as e:
        db.rollback()
        print(f"\n❌ Error de integridad: {e}")
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
