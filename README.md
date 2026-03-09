# SuperMarket API

Sistema backend para la gestión integral de una cadena de supermercados. 
Provee una API REST completa desarrollada en **FastAPI** para la administración de clientes, empleados, inventario, productos, sucursales, compras a proveedores y facturación en general.

## Características

- Gestión de Usuarios y Roles.
- Gestión de Inventario Multi-Sucursal (control de stock, límites mínimos).
- Gestión de Compras a Proveedores (integración con subida de inventario).
- Gestión de Facturación (Cabeceras y Detalles).
- Soft Delete integrado en todas las entidades principales.
- Menú de Interfaz de Comando (CLI) para administración rápida por consola.

## Requisitos

- Python 3.9+
- PostgreSQL
- FastAPI
- SQLAlchemy

## Mantenimiento

Para mantener el estándar de código del proyecto, utilizamos el formateador **Black**. 
Asegúrate de ejecutarlo antes de subir cambios.

### Comando para formatear el código:

```bash
black src/
```
