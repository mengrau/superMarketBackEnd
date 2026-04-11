# SuperMarket BackEnd

API REST para gestión de supermercado construida con FastAPI, SQLAlchemy y PostgreSQL.
Incluye autenticación JWT, migraciones con Alembic, seeders idempotentes y pruebas automatizadas.

## Propósito del repositorio

Este repositorio implementa el backend de un sistema de supermercados con operaciones para:

- autenticación y autorización por roles
- usuarios y empleados
- clientes, proveedores y productos
- inventario por sucursal
- compras a proveedor y facturación

El objetivo es mantener una base de código estable para desarrollo, CI/CD y despliegue.

## Estructura del proyecto

```text
superMarketBackEnd/
  .github/workflows/           # CI/CD
  alembic.ini                  # Configuración de Alembic
  bootstrap_db.py              # Migraciones + seeders
  migrate_db.py                # Solo migraciones
  seed_db.py                   # Solo seeders
  src/
    api/                       # Endpoints FastAPI
    core/                      # Núcleo (config, auth, errores, respuestas)
    crud/                      # Reglas de acceso a datos
    database/                  # Bootstrap/migraciones/seeders
    entities/                  # Modelos ORM
    migrations/                # Entorno y versiones de Alembic
    main.py                    # App FastAPI
    menu.py                    # Cliente de consola para consumir la API
    models.py                  # Schemas Pydantic
  tests/
```

## Requisitos

- Python 3.11 o superior
- PostgreSQL 15+ (o compatible)
- pip

## Instalación

1. Crear y activar entorno virtual.
2. Instalar dependencias.

```bash
pip install -r requirements.txt
```

## Configuración

Definir variables de entorno (archivo `.env` recomendado):

- `DATABASE_URL`: cadena de conexión a PostgreSQL.
- `SSL_MODE`: `require` (Neon/producción) o `disable` (local/CI).
- `JWT_SECRET_KEY`: clave de firma JWT.
- `JWT_ALGORITHM`: algoritmo de firma, por defecto `HS256`.
- `JWT_EXPIRE_MINUTES`: expiración del token en minutos, por defecto `60`.
- `CORS_ALLOW_ORIGINS`: orígenes permitidos separados por coma.
- `CORS_ALLOW_CREDENTIALS`: `true` o `false`.
- `RUN_SEEDERS_ON_STARTUP`: `true` o `false` para ejecutar seeders al iniciar API.
- `HTTP_CLIENT_BASE_URL`: URL base usada por `menu.py`.

## Ejecución

Levantar API:

```bash
uvicorn main:app --app-dir src --reload
```

URLs principales:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Cliente de consola (opcional):

```bash
python src/main.py
```

## Migraciones y seeders

El flujo recomendado es:

```bash
python migrate_db.py
python seed_db.py
```

O en un solo paso:

```bash
python bootstrap_db.py
```

### Comportamiento de seeders

- Idempotentes: no duplican datos si ya existen.
- Basados en claves de negocio (username, nit, identificación, código de barras, etc.).
- Mantienen relación de auditoría por `id_usuario_creacion`.
- Crean usuario administrador por defecto:
  - usuario: `admin`
  - contraseña: `admin123`

## Autenticación JWT

### Login

`POST /auth/login`

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Respuesta: `access_token`, `token_type`, `expires_in`.

### Uso de token

Enviar cabecera:

```http
Authorization: Bearer <access_token>
```

Validación de sesión actual:

- `GET /auth/me`

## Pruebas y calidad

Ejecutar validaciones locales:

```bash
ruff check src tests
ruff format src tests --check
pytest -q
```

## CI/CD

### CI

En rama `DEV` se ejecuta:

- instalación de dependencias
- `python bootstrap_db.py`
- lint y formato con Ruff
- pruebas con Pytest
- auditoría de dependencias con pip-audit

### CD

Se activa al completar CI exitosamente en `DEV` y publica imagen Docker en GHCR.

## Endpoints principales

- `/auth`
- `/usuarios`
- `/empleados`
- `/clientes`
- `/proveedores`
- `/productos`
- `/tipos-producto`
- `/sucursales`
- `/inventarios`
- `/compras-proveedor`
- `/facturas`
- `/roles`

## Notas de mantenimiento

- Mantener cambios de esquema vía Alembic.
- Evitar credenciales por defecto en entornos productivos.
- Ejecutar `bootstrap_db.py` en ambientes nuevos antes de pruebas funcionales.
