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
from crud.producto_crud import ProductoCRUD
from crud.proveedor_crud import ProveedorCRUD
from crud.sucursal_crud import SucursalCRUD
from crud.tipo_producto_crud import TipoProductoCRUD
from crud.usuario_crud import UsuarioCRUD


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


MENU_OPCIONES = {
    "1": ("Clientes", menu_clientes),
    "2": ("Productos", menu_productos),
    "3": ("Proveedores", menu_proveedores),
    "4": ("Sucursales", menu_sucursales),
    "5": ("Tipos de Producto", menu_tipos_producto),
    "6": ("Usuarios", menu_usuarios),
}


def iniciar_menu():
    """Punto de entrada del menú de consola."""
    while True:
        limpiar_pantalla()
        print("╔══════════════════════════════════════════╗")
        print("║     SUPERMERCADO — MENÚ PRINCIPAL        ║")
        print("╠══════════════════════════════════════════╣")
        for k, (label, _) in MENU_OPCIONES.items():
            print(f"║  {k}. {label:<39}║")
        print("║  7. Iniciar servidor FastAPI (API REST)   ║")
        print("║  0. Salir                                 ║")
        print("╚══════════════════════════════════════════╝")

        opcion = input("Opción: ").strip()

        if opcion in MENU_OPCIONES:
            _, fn = MENU_OPCIONES[opcion]
            fn()
        elif opcion == "7":
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
