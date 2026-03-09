"""
Menú de consola para gestión del Supermercado.
Permite interactuar con los CRUD de todas las entidades.
"""

import os
from decimal import Decimal, InvalidOperation
from typing import Optional
from uuid import UUID

from database.config import SessionLocal
from crud.cliente_crud import ClienteCRUD
from crud.compra_proveedor_crud import CompraProveedorCRUD
from crud.empleado_crud import EmpleadoCRUD
from crud.inventario_crud import InventarioCRUD
from crud.producto_crud import ProductoCRUD
from crud.proveedor_crud import ProveedorCRUD
from crud.sucursal_crud import SucursalCRUD
from crud.tipo_producto_crud import TipoProductoCRUD
from crud.usuario_crud import UsuarioCRUD
from crud.factura_crud import FacturaCRUD
from crud.rol_crud import RolCRUD


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresiona Enter para continuar...")


def leer_uuid(prompt: str) -> Optional[UUID]:
    """Solicita un UUID al usuario; devuelve None si está vacío."""
    while True:
        valor = input(prompt).strip()
        if not valor:
            return None
        try:
            return UUID(valor)
        except ValueError:
            print("  UUID inválido, intenta de nuevo (o presiona Enter para cancelar).")


def leer_uuid_opcional(prompt: str) -> Optional[UUID]:
    """Solicita un UUID opcional; ignora silenciosamente los UUIDs mal formados."""
    valor = input(prompt).strip()
    if not valor:
        return None
    try:
        return UUID(valor)
    except ValueError:
        print("  UUID inválido, se omitirá el campo.")
        return None


def separador(titulo: str):
    """Imprime un encabezado de sección con el título dado."""
    linea = "═" * 44
    print(f"\n╔{linea}╗")
    print(f"║  {titulo:<42}║")
    print(f"╚{linea}╝")


def menu_clientes():
    """Submenu de gestion de clientes: listar, crear, actualizar y eliminar."""
    while True:
        separador("CLIENTES")
        print("  1. Listar clientes")
        print("  2. Crear cliente")
        print("  3. Actualizar cliente")
        print("  4. Eliminar cliente (soft delete)")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = ClienteCRUD(db)
        try:
            if opcion == "1":
                clientes = crud.obtener_clientes()
                if not clientes:
                    print("  Sin registros.")
                for c in clientes:
                    print(
                        f"  [{c.id}]  {c.nombre}"
                        f"  |  {c.tipo_identificacion}: {c.identificacion}"
                        f"  |  Email: {c.email or '-'}"
                        f"  |  Tel: {c.telefono or '-'}"
                    )

            elif opcion == "2":
                nombre = input("  Nombre completo: ").strip()
                tipo_doc = input("  Tipo identificación (CC/NIT/CE): ").strip()
                identificacion = input("  Número de identificación: ").strip()
                email = input("  Email (opcional): ").strip() or None
                telefono = input("  Teléfono (opcional): ").strip() or None
                direccion = input("  Dirección (opcional): ").strip() or None
                c = crud.crear_cliente(
                    nombre, tipo_doc, identificacion, email, telefono, direccion
                )
                print(f"  ✔ Cliente creado — ID: {c.id}")

            elif opcion == "3":
                uid = leer_uuid("  UUID del cliente a actualizar: ")
                if uid is None:
                    print("  Operación cancelada.")
                else:
                    campos = {}
                    v = input("  Nuevo nombre (Enter para omitir): ").strip()
                    if v:
                        campos["nombre"] = v
                    v = input("  Nuevo email (Enter para omitir): ").strip()
                    if v:
                        campos["email"] = v
                    v = input("  Nuevo teléfono (Enter para omitir): ").strip()
                    if v:
                        campos["telefono"] = v
                    v = input("  Nueva dirección (Enter para omitir): ").strip()
                    if v:
                        campos["direccion"] = v
                    if campos:
                        r = crud.actualizar_cliente(uid, **campos)
                        print("  ✔ Actualizado." if r else "  ✘ Cliente no encontrado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del cliente a eliminar: ")
                if uid:
                    ok = crud.eliminar_cliente(uid)
                    print("  ✔ Eliminado." if ok else "  ✘ Cliente no encontrado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except ValueError as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_productos():
    """Submenu de gestion de productos: listar, crear, actualizar y eliminar."""
    while True:
        separador("PRODUCTOS")
        print("  1. Listar productos")
        print("  2. Crear producto")
        print("  3. Actualizar producto")
        print("  4. Eliminar producto (soft delete)")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = ProductoCRUD(db)
        try:
            if opcion == "1":
                productos = crud.obtener_productos()
                if not productos:
                    print("  Sin registros.")
                for p in productos:
                    print(
                        f"  [{p.id}]  {p.nombre}"
                        f"  |  ${p.precio_venta}"
                        f"  |  CB: {p.codigo_barras or '-'}"
                    )

            elif opcion == "2":
                nombre = input("  Nombre: ").strip()
                precio_str = input("  Precio de venta: ").strip()
                try:
                    precio = Decimal(precio_str)
                except InvalidOperation:
                    print("  Precio inválido.")
                    pausar()
                    continue
                codigo_barras = input("  Código de barras (opcional): ").strip() or None
                id_tipo = leer_uuid_opcional(
                    "  UUID tipo de producto (opcional, Enter para omitir): "
                )
                id_proveedor = leer_uuid_opcional(
                    "  UUID proveedor (opcional, Enter para omitir): "
                )
                p = crud.crear_producto(
                    nombre,
                    precio,
                    codigo_barras,
                    id_tipo=id_tipo,
                    id_proveedor=id_proveedor,
                )
                print(f"  ✔ Producto creado — ID: {p.id}")

            elif opcion == "3":
                uid = leer_uuid("  UUID del producto a actualizar: ")
                if uid is None:
                    print("  Operación cancelada.")
                else:
                    campos = {}
                    v = input("  Nuevo nombre (Enter para omitir): ").strip()
                    if v:
                        campos["nombre"] = v
                    v = input("  Nuevo precio (Enter para omitir): ").strip()
                    if v:
                        try:
                            campos["precio_venta"] = Decimal(v)
                        except InvalidOperation:
                            print("  Precio inválido, se omitirá.")
                    v = input("  Nuevo código de barras (Enter para omitir): ").strip()
                    if v:
                        campos["codigo_barras"] = v
                    if campos:
                        r = crud.actualizar_producto(uid, **campos)
                        print(
                            "  ✔ Actualizado." if r else "  ✘ Producto no encontrado."
                        )
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del producto a eliminar: ")
                if uid:
                    ok = crud.eliminar_producto(uid)
                    print("  ✔ Eliminado." if ok else "  ✘ Producto no encontrado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except ValueError as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_proveedores():
    """Submenu de gestion de proveedores: listar, crear, actualizar y eliminar."""
    while True:
        separador("PROVEEDORES")
        print("  1. Listar proveedores")
        print("  2. Crear proveedor")
        print("  3. Actualizar proveedor")
        print("  4. Eliminar proveedor (soft delete)")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = ProveedorCRUD(db)
        try:
            if opcion == "1":
                proveedores = crud.obtener_proveedores()
                if not proveedores:
                    print("  Sin registros.")
                for p in proveedores:
                    print(
                        f"  [{p.id}]  {p.nombre}"
                        f"  |  NIT: {p.nit}"
                        f"  |  {p.correo or '-'}"
                        f"  |  Tel: {p.telefono or '-'}"
                    )

            elif opcion == "2":
                nombre = input("  Nombre / Razón social: ").strip()
                nit = input("  NIT: ").strip()
                telefono = input("  Teléfono (opcional): ").strip() or None
                direccion = input("  Dirección (opcional): ").strip() or None
                correo = input("  Correo (opcional): ").strip() or None
                p = crud.crear_proveedor(nombre, nit, telefono, direccion, correo)
                print(f"  ✔ Proveedor creado — ID: {p.id}")

            elif opcion == "3":
                uid = leer_uuid("  UUID del proveedor a actualizar: ")
                if uid is None:
                    print("  Operación cancelada.")
                else:
                    campos = {}
                    v = input("  Nuevo nombre (Enter para omitir): ").strip()
                    if v:
                        campos["nombre"] = v
                    v = input("  Nuevo NIT (Enter para omitir): ").strip()
                    if v:
                        campos["nit"] = v
                    v = input("  Nuevo correo (Enter para omitir): ").strip()
                    if v:
                        campos["correo"] = v
                    v = input("  Nuevo teléfono (Enter para omitir): ").strip()
                    if v:
                        campos["telefono"] = v
                    if campos:
                        r = crud.actualizar_proveedor(uid, **campos)
                        print(
                            "  ✔ Actualizado." if r else "  ✘ Proveedor no encontrado."
                        )
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del proveedor a eliminar: ")
                if uid:
                    ok = crud.eliminar_proveedor(uid)
                    print("  ✔ Eliminado." if ok else "  ✘ Proveedor no encontrado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except ValueError as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_sucursales():
    """Submenu de gestion de sucursales: listar, crear, actualizar y eliminar."""
    while True:
        separador("SUCURSALES")
        print("  1. Listar sucursales")
        print("  2. Crear sucursal")
        print("  3. Actualizar sucursal")
        print("  4. Eliminar sucursal (soft delete)")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = SucursalCRUD(db)
        try:
            if opcion == "1":
                sucursales = crud.obtener_sucursales()
                if not sucursales:
                    print("  Sin registros.")
                for s in sucursales:
                    print(
                        f"  [{s.id}]  {s.nombre}"
                        f"  |  Dir: {s.direccion or '-'}"
                        f"  |  Gerente: {s.gerente or '-'}"
                        f"  |  Tel: {s.telefono or '-'}"
                    )

            elif opcion == "2":
                nombre = input("  Nombre: ").strip()
                direccion = input("  Dirección (opcional): ").strip() or None
                gerente = input("  Gerente (opcional): ").strip() or None
                telefono = input("  Teléfono (opcional): ").strip() or None
                s = crud.crear_sucursal(nombre, direccion, gerente, telefono)
                print(f"  ✔ Sucursal creada — ID: {s.id}")

            elif opcion == "3":
                uid = leer_uuid("  UUID de la sucursal a actualizar: ")
                if uid is None:
                    print("  Operación cancelada.")
                else:
                    campos = {}
                    v = input("  Nuevo nombre (Enter para omitir): ").strip()
                    if v:
                        campos["nombre"] = v
                    v = input("  Nueva dirección (Enter para omitir): ").strip()
                    if v:
                        campos["direccion"] = v
                    v = input("  Nuevo gerente (Enter para omitir): ").strip()
                    if v:
                        campos["gerente"] = v
                    v = input("  Nuevo teléfono (Enter para omitir): ").strip()
                    if v:
                        campos["telefono"] = v
                    if campos:
                        r = crud.actualizar_sucursal(uid, **campos)
                        print(
                            "  ✔ Actualizada." if r else "  ✘ Sucursal no encontrada."
                        )
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID de la sucursal a eliminar: ")
                if uid:
                    ok = crud.eliminar_sucursal(uid)
                    print("  ✔ Eliminada." if ok else "  ✘ Sucursal no encontrada.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except ValueError as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_tipos_producto():
    """Submenu de gestion de tipos de producto: listar, crear, actualizar y eliminar."""
    while True:
        separador("TIPOS DE PRODUCTO")
        print("  1. Listar tipos de producto")
        print("  2. Crear tipo de producto")
        print("  3. Actualizar tipo de producto")
        print("  4. Eliminar tipo de producto (soft delete)")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = TipoProductoCRUD(db)
        try:
            if opcion == "1":
                tipos = crud.obtener_tipos_producto()
                if not tipos:
                    print("  Sin registros.")
                for t in tipos:
                    print(f"  [{t.id}]  {t.nombre}" f"  |  {t.descripcion or '-'}")

            elif opcion == "2":
                nombre = input("  Nombre: ").strip()
                descripcion = input("  Descripción (opcional): ").strip() or None
                t = crud.crear_tipo_producto(nombre, descripcion)
                print(f"  ✔ Tipo de producto creado — ID: {t.id}")

            elif opcion == "3":
                uid = leer_uuid("  UUID del tipo a actualizar: ")
                if uid is None:
                    print("  Operación cancelada.")
                else:
                    campos = {}
                    v = input("  Nuevo nombre (Enter para omitir): ").strip()
                    if v:
                        campos["nombre"] = v
                    v = input("  Nueva descripción (Enter para omitir): ").strip()
                    if v:
                        campos["descripcion"] = v
                    if campos:
                        r = crud.actualizar_tipo_producto(uid, **campos)
                        print("  ✔ Actualizado." if r else "  ✘ Tipo no encontrado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del tipo a eliminar: ")
                if uid:
                    ok = crud.eliminar_tipo_producto(uid)
                    print("  ✔ Eliminado." if ok else "  ✘ Tipo no encontrado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except ValueError as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_usuarios():
    """Submenu de gestion de usuarios: listar, crear, actualizar, eliminar, cambiar contraseña y autenticar."""
    while True:
        separador("USUARIOS")
        print("  1. Listar usuarios")
        print("  2. Crear usuario")
        print("  3. Actualizar usuario")
        print("  4. Eliminar usuario (soft delete)")
        print("  5. Cambiar contraseña")
        print("  6. Autenticar usuario")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = UsuarioCRUD(db)
        try:
            if opcion == "1":
                usuarios = crud.obtener_usuarios()
                if not usuarios:
                    print("  Sin registros.")
                for u in usuarios:
                    print(f"  [{u.id}]  {u.username}" f"  |  Rol: {u.id_rol}")

            elif opcion == "2":
                username = input("  Username: ").strip()
                password = input("  Contraseña: ").strip()
                id_rol = leer_uuid("  UUID del rol (requerido): ")
                if id_rol is None:
                    print("  UUID del rol requerido — operación cancelada.")
                else:
                    u = crud.crear_usuario(username, password, id_rol)
                    print(f"  ✔ Usuario creado — ID: {u.id}")

            elif opcion == "3":
                uid = leer_uuid("  UUID del usuario a actualizar: ")
                if uid is None:
                    print("  Operación cancelada.")
                else:
                    campos = {}
                    v = input("  Nuevo username (Enter para omitir): ").strip()
                    if v:
                        campos["username"] = v
                    if campos:
                        r = crud.actualizar_usuario(uid, **campos)
                        print("  ✔ Actualizado." if r else "  ✘ Usuario no encontrado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del usuario a eliminar: ")
                if uid:
                    ok = crud.eliminar_usuario(uid)
                    print("  ✔ Eliminado." if ok else "  ✘ Usuario no encontrado.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "5":
                uid = leer_uuid("  UUID del usuario: ")
                if uid:
                    actual = input("  Contraseña actual: ").strip()
                    nueva = input("  Nueva contraseña: ").strip()
                    ok = crud.cambiar_contrasena(uid, actual, nueva)
                    print(
                        "  ✔ Contraseña actualizada."
                        if ok
                        else "  ✘ Usuario no encontrado."
                    )
                else:
                    print("  Operación cancelada.")

            elif opcion == "6":
                username = input("  Username: ").strip()
                password = input("  Contraseña: ").strip()
                u = crud.autenticar_usuario(username, password)
                if u:
                    print(
                        f"  ✔ Autenticación exitosa — {u.username}  |  Rol: {u.id_rol}"
                    )
                else:
                    print("  ✘ Credenciales incorrectas o usuario inactivo.")

            else:
                print("  Opción inválida.")

        except ValueError as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_empleados():
    """Submenu de gestion de empleados: listar, crear, actualizar y eliminar."""
    while True:
        separador("EMPLEADOS")
        print("  1. Listar empleados")
        print("  2. Crear empleado")
        print("  3. Actualizar empleado")
        print("  4. Eliminar empleado (soft delete)")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = EmpleadoCRUD(db)
        try:
            if opcion == "1":
                empleados = crud.obtener_empleados()
                if not empleados:
                    print("  Sin registros.")
                for e in empleados:
                    print(
                        f"  [{e.id}]  {e.nombre}"
                        f"  |  {e.tipo_identificacion}: {e.identificacion}"
                        f"  |  Cargo: {e.cargo or '-'}"
                        f"  |  User: {e.username}"
                    )

            elif opcion == "2":
                username = input("  Username: ").strip()
                password = input("  Contraseña: ").strip()
                id_rol = leer_uuid("  UUID del rol (requerido): ")
                if id_rol is None:
                    print("  UUID del rol requerido — operación cancelada.")
                    pausar()
                    continue
                nombre = input("  Nombre completo: ").strip()
                tipo_doc = input("  Tipo identificación (CC/NIT/CE): ").strip()
                identificacion = input("  Número de identificación: ").strip()
                telefono = input("  Teléfono (opcional): ").strip() or None
                direccion = input("  Dirección (opcional): ").strip() or None
                cargo = input("  Cargo (opcional): ").strip() or None
                salario = input("  Salario (opcional): ").strip() or None
                e = crud.crear_empleado(
                    username,
                    password,
                    id_rol,
                    nombre,
                    tipo_doc,
                    identificacion,
                    telefono,
                    direccion,
                    cargo,
                    salario,
                )
                print(f"  ✔ Empleado creado — ID: {e.id}")

            elif opcion == "3":
                uid = leer_uuid("  UUID del empleado a actualizar: ")
                if uid is None:
                    print("  Operación cancelada.")
                else:
                    campos = {}
                    v = input("  Nuevo nombre (Enter para omitir): ").strip()
                    if v:
                        campos["nombre"] = v
                    v = input("  Nuevo cargo (Enter para omitir): ").strip()
                    if v:
                        campos["cargo"] = v
                    v = input("  Nuevo salario (Enter para omitir): ").strip()
                    if v:
                        campos["salario"] = v
                    v = input("  Nuevo teléfono (Enter para omitir): ").strip()
                    if v:
                        campos["telefono"] = v
                    v = input("  Nueva dirección (Enter para omitir): ").strip()
                    if v:
                        campos["direccion"] = v
                    v = input("  Nueva contraseña (Enter para omitir): ").strip()
                    if v:
                        campos["password"] = v
                    if campos:
                        r = crud.actualizar_empleado(uid, **campos)
                        print(
                            "  ✔ Actualizado." if r else "  ✘ Empleado no encontrado."
                        )
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del empleado a eliminar: ")
                if uid:
                    ok = crud.eliminar_empleado(uid)
                    print("  ✔ Eliminado." if ok else "  ✘ Empleado no encontrado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except ValueError as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_inventario():
    """Submenú de gestión de inventario."""
    while True:
        separador("INVENTARIO")
        print("  1. Listar inventarios (activos)")
        print("  2. Buscar inventario por ID")
        print("  3. Buscar inventario por producto + sucursal")
        print("  4. Listar inventario de una sucursal")
        print("  5. Ver productos bajo stock mínimo")
        print("  6. Crear inventario")
        print("  7. Ajustar stock (sumar / restar)")
        print("  8. Actualizar inventario")
        print("  9. Desactivar inventario (soft delete)")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = InventarioCRUD(db)
        try:
            if opcion == "1":
                inventarios = crud.obtener_inventarios()
                if not inventarios:
                    print("  Sin registros.")
                for i in inventarios:
                    print(
                        f"  [{i.id}]"
                        f"  Prod: {i.id_producto}"
                        f"  |  Suc: {i.id_sucursal}"
                        f"  |  Stock: {i.stock_actual} (mín {i.stock_minimo})"
                        f"  |  Ubic: {i.ubicacion or '-'}"
                    )

            elif opcion == "2":
                uid = leer_uuid("  UUID del inventario: ")
                if uid:
                    inv = crud.obtener_inventario(uid)
                    if inv:
                        print(
                            f"  [{inv.id}]  Prod: {inv.id_producto}"
                            f"  |  Suc: {inv.id_sucursal}"
                            f"  |  Stock: {inv.stock_actual} (mín {inv.stock_minimo})"
                            f"  |  Ubic: {inv.ubicacion or '-'}"
                        )
                    else:
                        print("  ✘ No encontrado.")

            elif opcion == "3":
                id_prod = leer_uuid("  UUID del producto: ")
                id_suc = leer_uuid("  UUID de la sucursal: ")
                if id_prod and id_suc:
                    inv = crud.obtener_inventario_por_producto_sucursal(id_prod, id_suc)
                    if inv:
                        print(
                            f"  [{inv.id}]  Stock: {inv.stock_actual}"
                            f"  (mín {inv.stock_minimo})"
                            f"  |  Ubic: {inv.ubicacion or '-'}"
                        )
                    else:
                        print("  ✘ No existe inventario para esa combinación.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "4":
                id_suc = leer_uuid("  UUID de la sucursal: ")
                if id_suc:
                    inventarios = crud.obtener_inventarios_por_sucursal(id_suc)
                    if not inventarios:
                        print("  Sin registros.")
                    for i in inventarios:
                        print(
                            f"  [{i.id}]  Prod: {i.id_producto}"
                            f"  |  Stock: {i.stock_actual} (mín {i.stock_minimo})"
                            f"  |  Ubic: {i.ubicacion or '-'}"
                        )

            elif opcion == "5":
                id_suc = leer_uuid_opcional(
                    "  UUID de sucursal (opcional, Enter para todas): "
                )
                inventarios = crud.obtener_inventarios_bajo_minimo(id_sucursal=id_suc)
                if not inventarios:
                    print("  ✔ Ningún producto bajo el mínimo.")
                for i in inventarios:
                    print(
                        f"  [{i.id}]  Prod: {i.id_producto}"
                        f"  |  Suc: {i.id_sucursal}"
                        f"  |  Stock: {i.stock_actual} / Mín: {i.stock_minimo}"
                    )

            elif opcion == "6":
                id_prod = leer_uuid("  UUID del producto: ")
                id_suc = leer_uuid("  UUID de la sucursal: ")
                if not id_prod or not id_suc:
                    print("  Operación cancelada.")
                else:
                    stock_str = input("  Stock inicial (Enter = 0): ").strip() or "0"
                    minimo_str = input("  Stock mínimo (Enter = 0): ").strip() or "0"
                    ubicacion = input("  Ubicación (opcional): ").strip() or None
                    inv = crud.crear_inventario(
                        id_producto=id_prod,
                        id_sucursal=id_suc,
                        stock_actual=int(stock_str),
                        stock_minimo=int(minimo_str),
                        ubicacion=ubicacion,
                    )
                    print(f"  ✔ Inventario creado — ID: {inv.id}")

            elif opcion == "7":
                uid = leer_uuid("  UUID del inventario: ")
                if uid:
                    cant_str = input(
                        "  Cantidad a ajustar (positivo suma, negativo resta): "
                    ).strip()
                    inv = crud.ajustar_stock(uid, int(cant_str))
                    if inv:
                        print(f"  ✔ Stock actualizado: {inv.stock_actual}")
                    else:
                        print("  ✘ Inventario no encontrado.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "8":
                uid = leer_uuid("  UUID del inventario a actualizar: ")
                if uid is None:
                    print("  Operación cancelada.")
                else:
                    campos = {}
                    v = input("  Nuevo stock actual (Enter para omitir): ").strip()
                    if v:
                        campos["stock_actual"] = int(v)
                    v = input("  Nuevo stock mínimo (Enter para omitir): ").strip()
                    if v:
                        campos["stock_minimo"] = int(v)
                    v = input("  Nueva ubicación (Enter para omitir): ").strip()
                    if v:
                        campos["ubicacion"] = v
                    if campos:
                        inv = crud.actualizar_inventario(uid, **campos)
                        print("  ✔ Actualizado." if inv else "  ✘ No encontrado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "9":
                uid = leer_uuid("  UUID del inventario a desactivar: ")
                if uid:
                    ok = crud.eliminar_inventario(uid)
                    print("  ✔ Desactivado." if ok else "  ✘ No encontrado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except (ValueError, TypeError) as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_compras_proveedor():
    """Submenú de gestión de compras a proveedor y sus detalles."""
    while True:
        separador("COMPRAS PROVEEDOR")
        print("  1. Listar compras")
        print("  2. Buscar compra por ID")
        print("  3. Listar compras de un proveedor")
        print("  4. Crear compra")
        print("  5. Cambiar estado de compra")
        print("  6. Anular compra")
        print("  7. Ver detalles de una compra")
        print("  8. Agregar detalle a compra")
        print("  9. Eliminar detalle de compra")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = CompraProveedorCRUD(db)
        try:
            if opcion == "1":
                compras = crud.obtener_compras()
                if not compras:
                    print("  Sin registros.")
                for c in compras:
                    print(
                        f"  [{c.id}]"
                        f"  Prov: {c.id_proveedor}"
                        f"  |  Estado: {c.estado}"
                        f"  |  Total: ${c.total_compra}"
                        f"  |  Suc: {c.id_sucursal or '-'}"
                    )

            elif opcion == "2":
                uid = leer_uuid("  UUID de la compra: ")
                if uid:
                    c = crud.obtener_compra(uid)
                    if c:
                        print(
                            f"  [{c.id}]  Prov: {c.id_proveedor}"
                            f"  |  Estado: {c.estado}"
                            f"  |  Total: ${c.total_compra}"
                            f"  |  Fecha: {c.fecha}"
                            f"  |  Suc: {c.id_sucursal or '-'}"
                        )
                    else:
                        print("  ✘ No encontrada.")

            elif opcion == "3":
                id_prov = leer_uuid("  UUID del proveedor: ")
                if id_prov:
                    compras = crud.obtener_compras_por_proveedor(id_prov)
                    if not compras:
                        print("  Sin registros.")
                    for c in compras:
                        print(
                            f"  [{c.id}]  Estado: {c.estado}"
                            f"  |  Total: ${c.total_compra}"
                            f"  |  Suc: {c.id_sucursal or '-'}"
                        )

            elif opcion == "4":
                id_prov = leer_uuid("  UUID del proveedor: ")
                if not id_prov:
                    print("  Operación cancelada.")
                else:
                    id_suc = leer_uuid_opcional(
                        "  UUID de la sucursal destino (opcional, Enter para omitir): "
                    )
                    print(
                        "  Estado inicial: pedida / recibida (Enter = recibida): ",
                        end="",
                    )
                    estado = input().strip() or "recibida"
                    c = crud.crear_compra(
                        id_proveedor=id_prov,
                        id_sucursal=id_suc,
                        estado=estado,
                    )
                    print(f"  ✔ Compra creada — ID: {c.id}  Estado: {c.estado}")

            elif opcion == "5":
                uid = leer_uuid("  UUID de la compra: ")
                if uid:
                    print("  Nuevo estado (pedida / recibida / anulada): ", end="")
                    estado = input().strip()
                    c = crud.actualizar_compra(uid, estado=estado)
                    if c:
                        print(f"  ✔ Estado actualizado a: {c.estado}")
                    else:
                        print("  ✘ Compra no encontrada.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "6":
                uid = leer_uuid("  UUID de la compra a anular: ")
                if uid:
                    c = crud.anular_compra(uid)
                    if c:
                        print(f"  ✔ Compra anulada. Stock revertido si aplica.")
                    else:
                        print("  ✘ Compra no encontrada.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "7":
                uid = leer_uuid("  UUID de la compra: ")
                if uid:
                    detalles = crud.obtener_detalles_por_compra(uid)
                    if not detalles:
                        print("  Sin detalles registrados.")
                    for d in detalles:
                        print(
                            f"  [{d.id}]  Prod: {d.id_producto}"
                            f"  |  Cant: {d.cantidad}"
                            f"  |  P.Compra: ${d.precio_compra}"
                            f"  |  Sub: ${Decimal(str(d.precio_compra)) * d.cantidad}"
                        )

            elif opcion == "8":
                id_compra = leer_uuid("  UUID de la compra: ")
                if not id_compra:
                    print("  Operación cancelada.")
                else:
                    id_prod = leer_uuid("  UUID del producto: ")
                    if not id_prod:
                        print("  Operación cancelada.")
                    else:
                        cant_str = input("  Cantidad: ").strip()
                        precio_str = input("  Precio de compra por unidad: ").strip()
                        try:
                            d = crud.agregar_detalle(
                                id_compra=id_compra,
                                id_producto=id_prod,
                                cantidad=int(cant_str),
                                precio_compra=Decimal(precio_str),
                            )
                            print(f"  ✔ Detalle agregado — ID: {d.id}")
                        except InvalidOperation:
                            print("  ✘ Precio inválido.")

            elif opcion == "9":
                uid = leer_uuid("  UUID del detalle a eliminar: ")
                if uid:
                    ok = crud.eliminar_detalle(uid)
                    print(
                        "  ✔ Detalle eliminado. Stock ajustado si aplica."
                        if ok
                        else "  ✘ Detalle no encontrado."
                    )
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except (ValueError, TypeError) as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_facturas():
    """Submenú de gestión de facturas."""
    while True:
        separador("FACTURAS")
        print("  1. Listar facturas")
        print("  2. Buscar factura por ID")
        print("  3. Listar facturas de un cliente")
        print("  4. Crear factura")
        print("  5. Actualizar estado de factura")
        print("  6. Anular factura")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = FacturaCRUD(db)
        try:
            if opcion == "1":
                facturas = crud.obtener_facturas()
                if not facturas:
                    print("  Sin registros.")
                for f in facturas:
                    print(
                        f"  [{f.id}]"
                        f"  Cliente: {f.id_cliente}"
                        f"  |  Estado: {f.estado}"
                        f"  |  Total: ${f.total}"
                        f"  |  Suc: {f.id_sucursal or '-'}"
                    )

            elif opcion == "2":
                uid = leer_uuid("  UUID de la factura: ")
                if uid:
                    f = crud.obtener_factura(uid)
                    if f:
                        print(
                            f"  [{f.id}]  Cliente: {f.id_cliente}"
                            f"  |  Emp: {f.id_empleado}"
                            f"  |  Estado: {f.estado}"
                            f"  |  Total: ${f.total}"
                            f"  |  Pago: {f.metodo_pago or '-'}"
                            f"  |  Fecha: {f.fecha_creacion}"
                        )
                    else:
                        print("  ✘ No encontrada.")

            elif opcion == "3":
                id_cliente = leer_uuid("  UUID del cliente: ")
                if id_cliente:
                    facturas = crud.obtener_facturas_por_cliente(id_cliente)
                    if not facturas:
                        print("  Sin registros.")
                    for f in facturas:
                        print(
                            f"  [{f.id}]  Estado: {f.estado}"
                            f"  |  Total: ${f.total}"
                            f"  |  Suc: {f.id_sucursal or '-'}"
                        )

            elif opcion == "4":
                id_cliente = leer_uuid("  UUID del cliente: ")
                id_empleado = leer_uuid("  UUID del empleado: ")
                id_sucursal = leer_uuid("  UUID de la sucursal: ")

                if not id_cliente or not id_empleado or not id_sucursal:
                    print("  Operación cancelada. Faltan IDs requeridos.")
                else:
                    pago = (
                        input("  Método de pago (Enter para omitir): ").strip() or None
                    )
                    print(
                        "  Estado inicial: emitida / pendiente (Enter = emitida): ",
                        end="",
                    )
                    estado = input().strip() or "emitida"
                    f = crud.crear_factura(
                        id_cliente=id_cliente,
                        id_empleado=id_empleado,
                        id_sucursal=id_sucursal,
                        metodo_pago=pago,
                        estado=estado,
                    )
                    print(f"  ✔ Factura creada — ID: {f.id}  Estado: {f.estado}")

            elif opcion == "5":
                uid = leer_uuid("  UUID de la factura: ")
                if uid:
                    print("  Nuevo estado (emitida / pendiente / anulada): ", end="")
                    estado = input().strip()
                    f = crud.actualizar_factura(uid, estado=estado)
                    if f:
                        print(f"  ✔ Estado actualizado a: {f.estado}")
                    else:
                        print("  ✘ Factura no encontrada.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "6":
                uid = leer_uuid("  UUID de la factura a anular: ")
                if uid:
                    f = crud.anular_factura(uid)
                    if f:
                        print(f"  ✔ Factura anulada.")
                    else:
                        print("  ✘ Factura no encontrada.")
                else:
                    print("  Operación cancelada.")
            else:
                print("  Opción inválida.")

        except (ValueError, TypeError) as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_detalle_factura():
    """Submenú de gestión de detalles de factura."""
    while True:
        separador("DETALLE FACTURA")
        print("  1. Ver detalles de una factura")
        print("  2. Buscar detalle por ID")
        print("  3. Agregar detalle a factura")
        print("  4. Eliminar detalle")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = FacturaCRUD(db)
        try:
            if opcion == "1":
                id_factura = leer_uuid("  UUID de la factura: ")
                if not id_factura:
                    print("  Operación cancelada.")
                else:
                    detalles = crud.obtener_detalles_por_factura(id_factura)
                    if not detalles:
                        print("  Sin detalles registrados para esa factura.")
                    for d in detalles:
                        print(
                            f"  [{d.id}]"
                            f"  Prod: {d.id_producto}"
                            f"  |  Cant: {d.cantidad}"
                            f"  |  P.Unit: ${d.precio_unitario}"
                            f"  |  Sub: ${d.subtotal}"
                        )

            elif opcion == "2":
                uid = leer_uuid("  UUID del detalle: ")
                if uid:
                    d = crud.obtener_detalle(uid)
                    if d:
                        print(
                            f"  [{d.id}]"
                            f"  Factura: {d.id_factura}"
                            f"  |  Prod: {d.id_producto}"
                            f"  |  Cant: {d.cantidad}"
                            f"  |  P.Unit: ${d.precio_unitario}"
                            f"  |  Sub: ${d.subtotal}"
                            f"  |  Fecha: {d.fecha_creacion}"
                        )
                    else:
                        print("  ✘ Detalle no encontrado.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "3":
                id_factura = leer_uuid("  UUID de la factura: ")
                if not id_factura:
                    print("  Operación cancelada.")
                else:
                    id_prod = leer_uuid("  UUID del producto: ")
                    if not id_prod:
                        print("  Operación cancelada.")
                    else:
                        cant_str = input("  Cantidad: ").strip()
                        precio_str = input("  Precio unitario: ").strip()
                        try:
                            d = crud.agregar_detalle(
                                id_factura=id_factura,
                                id_producto=id_prod,
                                cantidad=int(cant_str),
                                precio_unitario=Decimal(precio_str),
                            )
                            print(
                                f"  ✔ Detalle agregado — ID: {d.id}"
                                f"  |  Subtotal: ${d.subtotal}"
                            )
                        except InvalidOperation:
                            print("  ✘ Precio inválido.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del detalle a eliminar: ")
                if uid:
                    ok = crud.eliminar_detalle(uid)
                    print(
                        "  ✔ Detalle eliminado. Total de factura actualizado."
                        if ok
                        else "  ✘ Detalle no encontrado."
                    )
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except (ValueError, TypeError) as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


def menu_roles():
    """Submenú de gestión de roles."""
    while True:
        separador("ROLES")
        print("  1. Listar roles")
        print("  2. Crear rol")
        print("  3. Actualizar rol")
        print("  4. Desactivar rol (soft delete)")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        db = SessionLocal()
        crud = RolCRUD(db)
        try:
            if opcion == "1":
                roles = crud.obtener_roles()
                if not roles:
                    print("  Sin registros.")
                for r in roles:
                    estado = "Activo" if r.activo else "Inactivo"
                    print(
                        f"  [{r.id}]  {r.nombre}"
                        f"  |  Estado: {estado}"
                        f"  |  Salario Base: ${r.salario or '0.00'}"
                    )

            elif opcion == "2":
                nombre = input("  Nombre del rol: ").strip()
                if not nombre:
                    print("  Operación cancelada. El nombre es obligatorio.")
                else:
                    descripcion = (
                        input("  Descripción (Enter para omitir): ").strip() or None
                    )
                    salario_str = input("  Salario base (Enter para omitir): ").strip()
                    salario = None
                    if salario_str:
                        try:
                            salario = float(salario_str)
                        except ValueError:
                            print("  Salario inválido, se guardará como Nulo.")

                    r = crud.crear_rol(nombre, descripcion, salario)
                    print(f"  ✔ Rol creado — ID: {r.id}")

            elif opcion == "3":
                uid = leer_uuid("  UUID del rol a actualizar: ")
                if uid:
                    campos = {}
                    v = input("  Nuevo nombre (Enter para omitir): ").strip()
                    if v:
                        campos["nombre"] = v
                    v = input("  Nueva descripción (Enter para omitir): ").strip()
                    if v:
                        campos["descripcion"] = v
                    v = input("  Nuevo salario (Enter para omitir): ").strip()
                    if v:
                        try:
                            campos["salario"] = float(v)
                        except ValueError:
                            print("  Salario inválido, se omitirá.")
                    v = input("  ¿Activo? (S/N) (Enter para omitir): ").strip().upper()
                    if v == "S":
                        campos["activo"] = True
                    elif v == "N":
                        campos["activo"] = False

                    if campos:
                        r = crud.actualizar_rol(uid, **campos)
                        if r:
                            print("  ✔ Rol actualizado.")
                        else:
                            print("  ✘ Rol no encontrado.")
                    else:
                        print("  Sin cambios.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del rol a desactivar: ")
                if uid:
                    ok = crud.eliminar_rol(uid)
                    if ok:
                        print("  ✔ Rol desactivado.")
                    else:
                        print("  ✘ Rol no encontrado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except (ValueError, TypeError) as e:
            print(f"  ✘ Error: {e}")
        finally:
            db.close()

        pausar()


MENU_OPCIONES = {
    "1": ("Clientes", menu_clientes),
    "2": ("Productos", menu_productos),
    "3": ("Proveedores", menu_proveedores),
    "4": ("Sucursales", menu_sucursales),
    "5": ("Tipos de Producto", menu_tipos_producto),
    "6": ("Usuarios", menu_usuarios),
    "7": ("Empleados", menu_empleados),
    "8": ("Inventario", menu_inventario),
    "9": ("Compras Proveedor", menu_compras_proveedor),
    "10": ("Detalle Factura", menu_detalle_factura),
    "11": ("Facturas Generales", menu_facturas),
    "12": ("Roles", menu_roles),
}


def iniciar_menu():
    """Punto de entrada del menú de consola."""
    while True:
        limpiar_pantalla()
        print("╔══════════════════════════════════════════╗")
        print("║     SUPERMERCADO — MENÚ PRINCIPAL        ║")
        print("╠══════════════════════════════════════════╣")
        for k, (label, _) in MENU_OPCIONES.items():
            print(f"║  {k}. {label:<37}║")
        print("║  13. Iniciar servidor FastAPI (API REST) ║")
        print("║  0. Salir                                ║")
        print("╚══════════════════════════════════════════╝")

        opcion = input("Opción: ").strip()

        if opcion in MENU_OPCIONES:
            _, fn = MENU_OPCIONES[opcion]
            fn()
        elif opcion == "13":
            import uvicorn

            print("\nIniciando servidor en http://localhost:8000 ...")
            print("Documentación: http://localhost:8000/docs")
            print("(Ctrl+C para detener)\n")
            uvicorn.run(
                "main:app",
                host="0.0.0.0",
                port=8000,
                reload=True,
                log_level="info",
            )
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción inválida.")
            pausar()
