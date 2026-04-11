"""
Menú de consola para gestión del Supermercado.
Consume la API REST de FastAPI en lugar de acceder directamente a la base de datos.

Antes de usar el menú asegúrate de que la API esté corriendo:
    uvicorn src.main:app --reload
o usa la opción 13 del menú principal para iniciarla.
"""

import os
from decimal import Decimal, InvalidOperation
from typing import Optional
from uuid import UUID

import http_client


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

        try:
            if opcion == "1":
                clientes = http_client.get("/clientes/", params={"limit": 200})
                if not clientes:
                    print("  Sin registros.")
                for c in clientes:
                    print(
                        f"  [{c['id']}]  {c['nombre']}"
                        f"  |  {c['identificacion']}"
                        f"  |  Email: {c.get('email') or '-'}"
                        f"  |  Tel: {c.get('telefono') or '-'}"
                    )

            elif opcion == "2":
                nombre = input("  Nombre completo: ").strip()
                identificacion = input("  Número de identificación: ").strip()
                email = input("  Email (opcional): ").strip() or None
                telefono = input("  Teléfono (opcional): ").strip() or None
                direccion = input("  Dirección (opcional): ").strip() or None
                c = http_client.post(
                    "/clientes/",
                    {
                        "nombre": nombre,
                        "identificacion": identificacion,
                        "email": email,
                        "telefono": telefono,
                        "direccion": direccion,
                    },
                )
                print(f"  ✔ Cliente creado — ID: {c['id']}")

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
                        http_client.put(f"/clientes/{uid}", campos)
                        print("  ✔ Actualizado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del cliente a eliminar: ")
                if uid:
                    http_client.delete(f"/clientes/{uid}")
                    print("  ✔ Eliminado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

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

        try:
            if opcion == "1":
                productos = http_client.get("/productos/", params={"limit": 200})
                if not productos:
                    print("  Sin registros.")
                for p in productos:
                    print(
                        f"  [{p['id']}]  {p['nombre']}"
                        f"  |  ${p['precio_venta']}"
                        f"  |  CB: {p.get('codigo_barras') or '-'}"
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
                p = http_client.post(
                    "/productos/",
                    {
                        "nombre": nombre,
                        "precio_venta": str(precio),
                        "codigo_barras": codigo_barras,
                        "id_tipo": str(id_tipo) if id_tipo else None,
                        "id_proveedor": str(id_proveedor) if id_proveedor else None,
                    },
                )
                print(f"  ✔ Producto creado — ID: {p['id']}")

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
                            campos["precio_venta"] = str(Decimal(v))
                        except InvalidOperation:
                            print("  Precio inválido, se omitirá.")
                    v = input("  Nuevo código de barras (Enter para omitir): ").strip()
                    if v:
                        campos["codigo_barras"] = v
                    if campos:
                        http_client.put(f"/productos/{uid}", campos)
                        print("  ✔ Actualizado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del producto a eliminar: ")
                if uid:
                    http_client.delete(f"/productos/{uid}")
                    print("  ✔ Eliminado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

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

        try:
            if opcion == "1":
                proveedores = http_client.get("/proveedores/", params={"limit": 200})
                if not proveedores:
                    print("  Sin registros.")
                for p in proveedores:
                    print(
                        f"  [{p['id']}]  {p['nombre']}"
                        f"  |  NIT: {p['nit']}"
                        f"  |  {p.get('correo') or '-'}"
                        f"  |  Tel: {p.get('telefono') or '-'}"
                    )

            elif opcion == "2":
                nombre = input("  Nombre / Razón social: ").strip()
                nit = input("  NIT: ").strip()
                telefono = input("  Teléfono (opcional): ").strip() or None
                direccion = input("  Dirección (opcional): ").strip() or None
                correo = input("  Correo (opcional): ").strip() or None
                p = http_client.post(
                    "/proveedores/",
                    {
                        "nombre": nombre,
                        "nit": nit,
                        "telefono": telefono,
                        "direccion": direccion,
                        "correo": correo,
                    },
                )
                print(f"  ✔ Proveedor creado — ID: {p['id']}")

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
                        http_client.put(f"/proveedores/{uid}", campos)
                        print("  ✔ Actualizado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del proveedor a eliminar: ")
                if uid:
                    http_client.delete(f"/proveedores/{uid}")
                    print("  ✔ Eliminado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

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

        try:
            if opcion == "1":
                sucursales = http_client.get("/sucursales/", params={"limit": 200})
                if not sucursales:
                    print("  Sin registros.")
                for s in sucursales:
                    print(
                        f"  [{s['id']}]  {s['nombre']}"
                        f"  |  Dir: {s.get('direccion') or '-'}"
                        f"  |  Gerente: {s.get('gerente') or '-'}"
                        f"  |  Tel: {s.get('telefono') or '-'}"
                    )

            elif opcion == "2":
                nombre = input("  Nombre: ").strip()
                direccion = input("  Dirección (opcional): ").strip() or None
                gerente = input("  Gerente (opcional): ").strip() or None
                telefono = input("  Teléfono (opcional): ").strip() or None
                s = http_client.post(
                    "/sucursales/",
                    {
                        "nombre": nombre,
                        "direccion": direccion,
                        "gerente": gerente,
                        "telefono": telefono,
                    },
                )
                print(f"  ✔ Sucursal creada — ID: {s['id']}")

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
                        http_client.put(f"/sucursales/{uid}", campos)
                        print("  ✔ Actualizada.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID de la sucursal a eliminar: ")
                if uid:
                    http_client.delete(f"/sucursales/{uid}")
                    print("  ✔ Eliminada.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

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

        try:
            if opcion == "1":
                tipos = http_client.get("/tipos-producto/", params={"limit": 200})
                if not tipos:
                    print("  Sin registros.")
                for t in tipos:
                    print(
                        f"  [{t['id']}]  {t['nombre']}  |  {t.get('descripcion') or '-'}"
                    )

            elif opcion == "2":
                nombre = input("  Nombre: ").strip()
                descripcion = input("  Descripción (opcional): ").strip() or None
                t = http_client.post(
                    "/tipos-producto/",
                    {
                        "nombre": nombre,
                        "descripcion": descripcion,
                    },
                )
                print(f"  ✔ Tipo de producto creado — ID: {t['id']}")

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
                        http_client.put(f"/tipos-producto/{uid}", campos)
                        print("  ✔ Actualizado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del tipo a eliminar: ")
                if uid:
                    http_client.delete(f"/tipos-producto/{uid}")
                    print("  ✔ Eliminado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

        pausar()


def menu_usuarios():
    """Submenu de gestion de usuarios: listar, crear, actualizar, eliminar y cambiar contraseña."""
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

        try:
            if opcion == "1":
                usuarios = http_client.get("/usuarios/")
                if not usuarios:
                    print("  Sin registros.")
                for u in usuarios:
                    print(f"  [{u['id']}]  {u['username']}  |  Rol: {u['id_rol']}")

            elif opcion == "2":
                username = input("  Username: ").strip()
                password = input("  Contraseña: ").strip()
                id_rol = leer_uuid("  UUID del rol (requerido): ")
                if id_rol is None:
                    print("  UUID del rol requerido — operación cancelada.")
                else:
                    u = http_client.post(
                        "/usuarios/",
                        {
                            "username": username,
                            "password": password,
                            "id_rol": str(id_rol),
                        },
                    )
                    print(f"  ✔ Usuario creado — ID: {u['id']}")

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
                        http_client.put(f"/usuarios/{uid}", campos)
                        print("  ✔ Actualizado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del usuario a eliminar: ")
                if uid:
                    http_client.delete(f"/usuarios/{uid}")
                    print("  ✔ Eliminado.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "5":
                uid = leer_uuid("  UUID del usuario: ")
                if uid:
                    nueva = input("  Nueva contraseña: ").strip()
                    http_client.put(f"/usuarios/{uid}", {"password": nueva})
                    print("  ✔ Contraseña actualizada.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "6":
                print(
                    "  ⚠ Autenticación no disponible via API REST "
                    "(endpoint no implementado en los routers actuales)."
                )
                print("  Usa POST /auth/login si agregas un router de autenticación.")

            else:
                print("  Opción inválida.")

        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

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

        try:
            if opcion == "1":
                empleados = http_client.get("/empleados/", params={"limit": 200})
                if not empleados:
                    print("  Sin registros.")
                for e in empleados:
                    print(
                        f"  [{e['id']}]  {e['nombre']}"
                        f"  |  {e.get('tipo_identificacion', '')}: {e['identificacion']}"
                        f"  |  Cargo: {e.get('cargo') or '-'}"
                        f"  |  User: {e['username']}"
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
                e = http_client.post(
                    "/empleados/",
                    {
                        "username": username,
                        "password": password,
                        "id_rol": str(id_rol),
                        "nombre": nombre,
                        "tipo_identificacion": tipo_doc,
                        "identificacion": identificacion,
                        "telefono": telefono,
                        "direccion": direccion,
                        "cargo": cargo,
                        "salario": salario,
                    },
                )
                print(f"  ✔ Empleado creado — ID: {e['id']}")

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
                        http_client.put(f"/empleados/{uid}", campos)
                        print("  ✔ Actualizado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del empleado a eliminar: ")
                if uid:
                    http_client.delete(f"/empleados/{uid}")
                    print("  ✔ Eliminado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

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

        try:
            if opcion == "1":
                inventarios = http_client.get(
                    "/inventarios/", params={"limit": 200, "solo_activos": True}
                )
                if not inventarios:
                    print("  Sin registros.")
                for i in inventarios:
                    print(
                        f"  [{i['id']}]"
                        f"  Prod: {i['id_producto']}"
                        f"  |  Suc: {i['id_sucursal']}"
                        f"  |  Stock: {i['stock_actual']} (mín {i['stock_minimo']})"
                        f"  |  Ubic: {i.get('ubicacion') or '-'}"
                    )

            elif opcion == "2":
                uid = leer_uuid("  UUID del inventario: ")
                if uid:
                    inv = http_client.get(f"/inventarios/{uid}")
                    print(
                        f"  [{inv['id']}]  Prod: {inv['id_producto']}"
                        f"  |  Suc: {inv['id_sucursal']}"
                        f"  |  Stock: {inv['stock_actual']} (mín {inv['stock_minimo']})"
                        f"  |  Ubic: {inv.get('ubicacion') or '-'}"
                    )
                else:
                    print("  Operación cancelada.")

            elif opcion == "3":
                id_prod = leer_uuid("  UUID del producto: ")
                id_suc = leer_uuid("  UUID de la sucursal: ")
                if id_prod and id_suc:
                    inventarios = http_client.get(
                        f"/inventarios/sucursal/{id_suc}", params={"limit": 500}
                    )
                    coincidencias = [
                        i for i in inventarios if i["id_producto"] == str(id_prod)
                    ]
                    if coincidencias:
                        inv = coincidencias[0]
                        print(
                            f"  [{inv['id']}]  Stock: {inv['stock_actual']}"
                            f"  (mín {inv['stock_minimo']})"
                            f"  |  Ubic: {inv.get('ubicacion') or '-'}"
                        )
                    else:
                        print("  ✘ No existe inventario para esa combinación.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "4":
                id_suc = leer_uuid("  UUID de la sucursal: ")
                if id_suc:
                    inventarios = http_client.get(
                        f"/inventarios/sucursal/{id_suc}", params={"limit": 200}
                    )
                    if not inventarios:
                        print("  Sin registros.")
                    for i in inventarios:
                        print(
                            f"  [{i['id']}]  Prod: {i['id_producto']}"
                            f"  |  Stock: {i['stock_actual']} (mín {i['stock_minimo']})"
                            f"  |  Ubic: {i.get('ubicacion') or '-'}"
                        )
                else:
                    print("  Operación cancelada.")

            elif opcion == "5":
                id_suc = leer_uuid_opcional(
                    "  UUID de sucursal (opcional, Enter para todas): "
                )
                params = {}
                if id_suc:
                    params["id_sucursal"] = str(id_suc)
                inventarios = http_client.get("/inventarios/bajo-minimo", params=params)
                if not inventarios:
                    print("  ✔ Ningún producto bajo el mínimo.")
                for i in inventarios:
                    print(
                        f"  [{i['id']}]  Prod: {i['id_producto']}"
                        f"  |  Suc: {i['id_sucursal']}"
                        f"  |  Stock: {i['stock_actual']} / Mín: {i['stock_minimo']}"
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
                    inv = http_client.post(
                        "/inventarios/",
                        {
                            "id_producto": str(id_prod),
                            "id_sucursal": str(id_suc),
                            "stock_actual": int(stock_str),
                            "stock_minimo": int(minimo_str),
                            "ubicacion": ubicacion,
                        },
                    )
                    print(f"  ✔ Inventario creado — ID: {inv['id']}")

            elif opcion == "7":
                uid = leer_uuid("  UUID del inventario: ")
                if uid:
                    cant_str = input(
                        "  Cantidad a ajustar (positivo suma, negativo resta): "
                    ).strip()
                    inv = http_client.patch(
                        f"/inventarios/{uid}/ajustar-stock",
                        params={"cantidad": int(cant_str)},
                    )
                    print(f"  ✔ Stock actualizado: {inv['stock_actual']}")
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
                        http_client.put(f"/inventarios/{uid}", campos)
                        print("  ✔ Actualizado.")
                    else:
                        print("  Sin cambios.")

            elif opcion == "9":
                uid = leer_uuid("  UUID del inventario a desactivar: ")
                if uid:
                    http_client.delete(f"/inventarios/{uid}")
                    print("  ✔ Desactivado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except (ValueError, TypeError) as e:
            print(f"  ✘ Error: {e}")
        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

        pausar()


def menu_compras_proveedor():
    """Submenú de gestión de compras a proveedor y sus detalles."""
    while True:
        separador("COMPRAS PROVEEDOR")
        print("  1. Listar compras")
        print("  2. Buscar compra por ID")
        print("  3. Listar compras de un proveedor")
        print("  4. Crear compra (con detalles)")
        print("  5. Cambiar estado de compra")
        print("  6. Anular compra")
        print("  7. Ver detalles de una compra")
        print("  8. Agregar detalle a compra")
        print("  9. Eliminar detalle de compra")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        try:
            if opcion == "1":
                compras = http_client.get("/compras-proveedor/", params={"limit": 200})
                if not compras:
                    print("  Sin registros.")
                for c in compras:
                    print(
                        f"  [{c['id']}]"
                        f"  Prov: {c['id_proveedor']}"
                        f"  |  Estado: {c['estado']}"
                        f"  |  Total: ${c['total_compra']}"
                        f"  |  Suc: {c.get('id_sucursal') or '-'}"
                    )

            elif opcion == "2":
                uid = leer_uuid("  UUID de la compra: ")
                if uid:
                    c = http_client.get(f"/compras-proveedor/{uid}")
                    print(
                        f"  [{c['id']}]  Prov: {c['id_proveedor']}"
                        f"  |  Estado: {c['estado']}"
                        f"  |  Total: ${c['total_compra']}"
                        f"  |  Fecha: {c.get('fecha')}"
                        f"  |  Suc: {c.get('id_sucursal') or '-'}"
                    )
                else:
                    print("  Operación cancelada.")

            elif opcion == "3":
                id_prov = leer_uuid("  UUID del proveedor: ")
                if id_prov:
                    compras = http_client.get(
                        f"/compras-proveedor/proveedor/{id_prov}",
                        params={"limit": 200},
                    )
                    if not compras:
                        print("  Sin registros.")
                    for c in compras:
                        print(
                            f"  [{c['id']}]  Estado: {c['estado']}"
                            f"  |  Total: ${c['total_compra']}"
                            f"  |  Suc: {c.get('id_sucursal') or '-'}"
                        )
                else:
                    print("  Operación cancelada.")

            elif opcion == "4":
                id_prov = leer_uuid("  UUID del proveedor: ")
                if not id_prov:
                    print("  Operación cancelada.")
                else:
                    id_suc = leer_uuid_opcional(
                        "  UUID de la sucursal destino (opcional, Enter para omitir): "
                    )
                    detalles = []
                    print("  Agregar productos (Enter en UUID para terminar):")
                    while True:
                        id_prod = leer_uuid_opcional(
                            "    UUID del producto (Enter para terminar): "
                        )
                        if not id_prod:
                            break
                        cant_str = input("    Cantidad: ").strip()
                        precio_str = input("    Precio de compra: ").strip()
                        try:
                            detalles.append(
                                {
                                    "id_producto": str(id_prod),
                                    "cantidad": int(cant_str),
                                    "precio_compra": precio_str,
                                }
                            )
                        except (ValueError, InvalidOperation):
                            print("    Datos inválidos, se omitirá este detalle.")
                    c = http_client.post(
                        "/compras-proveedor/",
                        {
                            "id_proveedor": str(id_prov),
                            "id_sucursal": str(id_suc) if id_suc else None,
                            "detalles": detalles,
                        },
                    )
                    print(f"  ✔ Compra creada — ID: {c['id']}  Estado: {c['estado']}")

            elif opcion == "5":
                uid = leer_uuid("  UUID de la compra: ")
                if uid:
                    print("  Nuevo estado (pedida / recibida / anulada): ", end="")
                    estado = input().strip()
                    c = http_client.put(f"/compras-proveedor/{uid}", {"estado": estado})
                    print(f"  ✔ Estado actualizado a: {c['estado']}")
                else:
                    print("  Operación cancelada.")

            elif opcion == "6":
                uid = leer_uuid("  UUID de la compra a anular: ")
                if uid:
                    http_client.patch(f"/compras-proveedor/{uid}/anular")
                    print("  ✔ Compra anulada. Stock revertido si aplica.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "7":
                uid = leer_uuid("  UUID de la compra: ")
                if uid:
                    detalles = http_client.get(f"/compras-proveedor/{uid}/detalles")
                    if not detalles:
                        print("  Sin detalles registrados.")
                    for d in detalles:
                        subtotal = Decimal(str(d["precio_compra"])) * d["cantidad"]
                        print(
                            f"  [{d['id']}]  Prod: {d['id_producto']}"
                            f"  |  Cant: {d['cantidad']}"
                            f"  |  P.Compra: ${d['precio_compra']}"
                            f"  |  Sub: ${subtotal}"
                        )
                else:
                    print("  Operación cancelada.")

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
                            d = http_client.post(
                                f"/compras-proveedor/{id_compra}/detalles",
                                {
                                    "id_producto": str(id_prod),
                                    "cantidad": int(cant_str),
                                    "precio_compra": precio_str,
                                },
                            )
                            print(f"  ✔ Detalle agregado — ID: {d['id']}")
                        except InvalidOperation:
                            print("  ✘ Precio inválido.")

            elif opcion == "9":
                uid = leer_uuid("  UUID del detalle a eliminar: ")
                if uid:
                    http_client.delete(f"/compras-proveedor/detalles/{uid}")
                    print("  ✔ Detalle eliminado. Stock ajustado si aplica.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except (ValueError, TypeError) as e:
            print(f"  ✘ Error: {e}")
        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

        pausar()


def menu_facturas():
    """Submenú de gestión de facturas y sus detalles."""
    while True:
        separador("FACTURAS")
        print("  1. Listar facturas")
        print("  2. Buscar factura por ID")
        print("  3. Listar facturas de un cliente")
        print("  4. Crear factura (con detalles)")
        print("  5. Actualizar estado de factura")
        print("  6. Anular factura")
        print("  7. Ver detalles de una factura")
        print("  8. Buscar detalle por ID")
        print("  9. Agregar detalle a factura")
        print("  10. Eliminar detalle")
        print("  0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "0":
            break

        try:
            if opcion == "1":
                facturas = http_client.get("/facturas/", params={"limit": 200})
                if not facturas:
                    print("  Sin registros.")
                for f in facturas:
                    print(
                        f"  [{f['id']}]"
                        f"  Cliente: {f['id_cliente']}"
                        f"  |  Estado: {f['estado']}"
                        f"  |  Total: ${f['total']}"
                        f"  |  Suc: {f.get('id_sucursal') or '-'}"
                    )

            elif opcion == "2":
                uid = leer_uuid("  UUID de la factura: ")
                if uid:
                    f = http_client.get(f"/facturas/{uid}")
                    print(
                        f"  [{f['id']}]  Cliente: {f['id_cliente']}"
                        f"  |  Emp: {f['id_empleado']}"
                        f"  |  Estado: {f['estado']}"
                        f"  |  Total: ${f['total']}"
                        f"  |  Pago: {f.get('metodo_pago') or '-'}"
                        f"  |  Fecha: {f.get('fecha_creacion')}"
                    )
                else:
                    print("  Operación cancelada.")

            elif opcion == "3":
                id_cliente = leer_uuid("  UUID del cliente: ")
                if id_cliente:
                    facturas = http_client.get(
                        f"/facturas/cliente/{id_cliente}", params={"limit": 200}
                    )
                    if not facturas:
                        print("  Sin registros.")
                    for f in facturas:
                        print(
                            f"  [{f['id']}]  Estado: {f['estado']}"
                            f"  |  Total: ${f['total']}"
                            f"  |  Suc: {f.get('id_sucursal') or '-'}"
                        )
                else:
                    print("  Operación cancelada.")

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
                    detalles = []
                    print("  Agregar productos (Enter en UUID para terminar):")
                    while True:
                        id_prod = leer_uuid_opcional(
                            "    UUID del producto (Enter para terminar): "
                        )
                        if not id_prod:
                            break
                        cant_str = input("    Cantidad: ").strip()
                        precio_str = input("    Precio unitario: ").strip()
                        try:
                            detalles.append(
                                {
                                    "id_producto": str(id_prod),
                                    "cantidad": int(cant_str),
                                    "precio_unitario": precio_str,
                                }
                            )
                        except (ValueError, InvalidOperation):
                            print("    Datos inválidos, se omitirá este detalle.")
                    f = http_client.post(
                        "/facturas/",
                        {
                            "id_cliente": str(id_cliente),
                            "id_empleado": str(id_empleado),
                            "id_sucursal": str(id_sucursal),
                            "metodo_pago": pago,
                            "detalles": detalles,
                        },
                    )
                    print(f"  ✔ Factura creada — ID: {f['id']}  Total: ${f['total']}")

            elif opcion == "5":
                uid = leer_uuid("  UUID de la factura: ")
                if uid:
                    print("  Nuevo estado (emitida / pendiente / anulada): ", end="")
                    estado = input().strip()
                    f = http_client.put(f"/facturas/{uid}", {"estado": estado})
                    print(f"  ✔ Estado actualizado a: {f['estado']}")
                else:
                    print("  Operación cancelada.")

            elif opcion == "6":
                uid = leer_uuid("  UUID de la factura a anular: ")
                if uid:
                    http_client.patch(f"/facturas/{uid}/anular")
                    print("  ✔ Factura anulada.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "7":
                uid = leer_uuid("  UUID de la factura: ")
                if uid:
                    detalles = http_client.get(f"/facturas/{uid}/detalles")
                    if not detalles:
                        print("  Sin detalles registrados.")
                    for d in detalles:
                        print(
                            f"  [{d['id']}]"
                            f"  Prod: {d['id_producto']}"
                            f"  |  Cant: {d['cantidad']}"
                            f"  |  P.Unit: ${d['precio_unitario']}"
                            f"  |  Sub: ${d['subtotal']}"
                        )
                else:
                    print("  Operación cancelada.")

            elif opcion == "8":
                uid = leer_uuid("  UUID del detalle: ")
                if uid:
                    d = http_client.get(f"/facturas/detalles/{uid}")
                    print(
                        f"  [{d['id']}]"
                        f"  Factura: {d['id_factura']}"
                        f"  |  Prod: {d['id_producto']}"
                        f"  |  Cant: {d['cantidad']}"
                        f"  |  P.Unit: ${d['precio_unitario']}"
                        f"  |  Sub: ${d['subtotal']}"
                    )
                else:
                    print("  Operación cancelada.")

            elif opcion == "9":
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
                            d = http_client.post(
                                f"/facturas/{id_factura}/detalles",
                                {
                                    "id_producto": str(id_prod),
                                    "cantidad": int(cant_str),
                                    "precio_unitario": precio_str,
                                },
                            )
                            print(
                                f"  ✔ Detalle agregado — ID: {d['id']}"
                                f"  |  Subtotal: ${d['subtotal']}"
                            )
                        except InvalidOperation:
                            print("  ✘ Precio inválido.")

            elif opcion == "10":
                uid = leer_uuid("  UUID del detalle a eliminar: ")
                if uid:
                    http_client.delete(f"/facturas/detalles/{uid}")
                    print("  ✔ Detalle eliminado. Total de factura actualizado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except (ValueError, TypeError) as e:
            print(f"  ✘ Error: {e}")
        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

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

        try:
            if opcion == "1":
                roles = http_client.get("/roles/", params={"limit": 200})
                if not roles:
                    print("  Sin registros.")
                for r in roles:
                    estado = "Activo" if r.get("activo") else "Inactivo"
                    print(
                        f"  [{r['id']}]  {r['nombre']}"
                        f"  |  Estado: {estado}"
                        f"  |  Salario Base: ${r.get('salario') or '0.00'}"
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

                    r = http_client.post(
                        "/roles/",
                        {
                            "nombre": nombre,
                            "descripcion": descripcion,
                            "salario": salario,
                        },
                    )
                    print(f"  ✔ Rol creado — ID: {r['id']}")

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
                        http_client.put(f"/roles/{uid}", campos)
                        print("  ✔ Rol actualizado.")
                    else:
                        print("  Sin cambios.")
                else:
                    print("  Operación cancelada.")

            elif opcion == "4":
                uid = leer_uuid("  UUID del rol a desactivar: ")
                if uid:
                    http_client.delete(f"/roles/{uid}")
                    print("  ✔ Rol desactivado.")
                else:
                    print("  Operación cancelada.")

            else:
                print("  Opción inválida.")

        except (ValueError, TypeError) as e:
            print(f"  ✘ Error: {e}")
        except RuntimeError as e:
            print(f"  ✘ Error: {e}")
        except Exception as e:
            print(f"  ✘ Error inesperado: {e}")

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
    "10": ("Facturas", menu_facturas),
    "11": ("Roles", menu_roles),
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
        print("║  12. Iniciar servidor FastAPI (API REST) ║")
        print("║  0. Salir                                ║")
        print("╚══════════════════════════════════════════╝")

        opcion = input("Opción: ").strip()

        if opcion in MENU_OPCIONES:
            _, fn = MENU_OPCIONES[opcion]
            fn()
        elif opcion == "12":
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
