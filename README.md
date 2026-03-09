# SuperMarket API

Sistema backend para la gestión integral de una cadena de supermercados.
Provee una API REST completa desarrollada en **FastAPI** para la administración de clientes, empleados, inventario, productos, sucursales, compras a proveedores y facturación en general.

## Características

- Gestión de Usuarios y Roles.
- Gestión de Inventario Multi-Sucursal (control de stock, límites mínimos).
- Gestión de Compras a Proveedores (integración con subida de inventario).
- Gestión de Facturación (Cabeceras y Detalles).
- Soft Delete integrado en todas las entidades principales.
- Menú de Interfaz de Comando (CLI) que consume la API REST vía HTTP.

## Requisitos

- Python 3.9+
- PostgreSQL
- FastAPI
- SQLAlchemy

## Cómo ejecutar

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Iniciar la API REST

Desde la raíz del proyecto:

```bash
uvicorn src.main:app --reload
```

La API quedará disponible en `http://localhost:8000`.  
Documentación interactiva en: `http://localhost:8000/docs`

### 3. Iniciar el menú de consola

En otra terminal (con la API ya corriendo):

```bash
python src/main.py
```

O directamente desde el menú principal, usa la **opción 13** para iniciar el servidor y luego ejecuta el menú en otra terminal.

> **Nota:** El menú requiere que la API esté corriendo en `http://localhost:8000`.  
> Para apuntar a otra URL, define la variable de entorno `HTTP_CLIENT_BASE_URL`:
>
> ```bash
> set HTTP_CLIENT_BASE_URL=http://mi-servidor:8000   # Windows
> export HTTP_CLIENT_BASE_URL=http://mi-servidor:8000 # Linux/Mac
> ```

## Pruebas manuales rápidas

1. Iniciar la API y abrir `http://localhost:8000/docs`.
2. Crear un rol vía el menú (opción 12 → opción 2) o via `/docs`.
3. Listar roles con la opción 12 → opción 1 y verificar que aparece el registro creado.
4. Actualizar el rol y confirmar el cambio consultando nuevamente la lista.
5. Repetir para clientes, productos, empleados, etc.

## Observaciones

Consulta la documentación interactiva en `http://localhost:8000/docs` para la lista completa de endpoints, ejemplos y esquema de datos.

## Mantenimiento

Para mantener el estándar de código del proyecto, utilizamos el formateador **Black**.
Asegúrate de ejecutarlo antes de subir cambios.

### Comando para formatear el código:

```bash
black src/
```
