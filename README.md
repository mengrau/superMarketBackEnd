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

- Python 3.11+
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

## Sincronización de BD y seeders

El proyecto incluye comandos para mantener el esquema actualizado y cargar datos iniciales idempotentes.

```bash
python cli.py migrate
python cli.py seed
python cli.py bootstrap-db
```

- `migrate`: aplica migraciones de Alembic hasta `head`.
- `seed`: inserta datos base sin duplicar registros existentes.
- `bootstrap-db`: ejecuta migraciones y luego seeders.

## Observaciones

Consulta la documentación interactiva en `http://localhost:8000/docs` para la lista completa de endpoints, ejemplos y esquema de datos.

## Mantenimiento

Para mantener el estándar de código del proyecto, utiliza Ruff para lint y formato.

### Comandos recomendados:

```bash
ruff check src tests
ruff format src tests
pytest -q
```

## CI/CD

El workflow de CI ejecuta, en la rama `DEV`:

- Migraciones y seed inicial (`python cli.py bootstrap-db`)
- Lint y validación de formato con Ruff
- Pruebas con Pytest
- Auditoría de dependencias con pip-audit

El workflow de CD se dispara únicamente cuando el CI de `DEV` finaliza exitosamente.

## Autenticación JWT

La API implementa autenticación Bearer con JWT.

### Variables de entorno JWT

- `JWT_SECRET_KEY`: clave secreta para firmar tokens (obligatoria en producción).
- `JWT_ALGORITHM`: algoritmo de firma (por defecto `HS256`).
- `JWT_EXPIRE_MINUTES`: tiempo de expiración del token en minutos (por defecto `60`).

### Flujo de login

1. Hacer `POST /auth/login` con usuario y contraseña:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

2. La API responde un `access_token`.
3. En rutas protegidas, enviar cabecera:

```http
Authorization: Bearer <access_token>
```

4. Puedes validar el token actual con `GET /auth/me`.

## Política CORS

La configuración CORS se controla por variables de entorno:

- `CORS_ALLOW_ORIGINS`: lista separada por comas de orígenes permitidos.
  - Ejemplo: `http://localhost:3000,http://127.0.0.1:5173`
- `CORS_ALLOW_CREDENTIALS`: `true` o `false` (por defecto `true`).

Reglas aplicadas:

- Cuando se usan credenciales, no se permite comodín global en producción.
- Se habilitan métodos necesarios: `GET, POST, PUT, PATCH, DELETE, OPTIONS`.
- Se habilitan cabeceras necesarias, incluyendo `Authorization`.
