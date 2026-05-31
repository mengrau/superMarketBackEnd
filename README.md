# SuperMarket BackEnd

Backend de gestión de supermercado construido con FastAPI, SQLAlchemy y PostgreSQL.

Incluye:

- API REST completa para operación diaria de negocio.
- Autenticación JWT con autorización por usuario activo.
- Migraciones con Alembic.
- Seeders idempotentes para entorno inicial.
- Menú de consola para consumir la API.
- Pipeline de CI/CD con pruebas, lint, auditoría de seguridad y publicación de imagen Docker en GHCR.
- Despliegue publico en Render y consumo desde el frontend desplegado en GitHub Pages.

## Tabla de contenido

- [Video demo](#video-demo)
- [URLs publicas](#urls-publicas)
- [Visión general](#visión-general)
- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Stack tecnológico](#stack-tecnológico)
- [Módulos funcionales](#módulos-funcionales)
- [Mapa de endpoints](#mapa-de-endpoints)
- [Autenticación y autorización](#autenticación-y-autorización)
- [Variables de entorno](#variables-de-entorno)
- [Instalación y ejecución local](#instalación-y-ejecución-local)
- [Migraciones y seeders](#migraciones-y-seeders)
- [Uso del menú de consola](#uso-del-menú-de-consola)
- [Ejecución con Docker](#ejecución-con-docker)
- [Pruebas, lint y seguridad](#pruebas-lint-y-seguridad)
- [CI/CD](#cicd)
- [Despliegue en Render](#despliegue-en-render)
- [Troubleshooting](#troubleshooting)
- [Buenas prácticas operativas](#buenas-prácticas-operativas)

## Video demo

[![Ver video demo en YouTube](https://img.youtube.com/vi/toM-GmfHZpo/hqdefault.jpg)](https://youtu.be/toM-GmfHZpo)

Si la vista previa no carga, puedes abrirlo directamente aquí: https://youtu.be/toM-GmfHZpo

## URLs publicas

- Backend en produccion: https://supermarketbackend.onrender.com
- Swagger en produccion: https://supermarketbackend.onrender.com/docs
- ReDoc en produccion: https://supermarketbackend.onrender.com/redoc
- Frontend en produccion: https://santi-osp.github.io/superMarketFrontEnd/

## Visión general

Este proyecto implementa el backend de una plataforma de supermercado con soporte para:

- Gestión de clientes, productos, proveedores, sucursales y tipos de producto.
- Gestión de inventario por sucursal, incluyendo ajuste de stock y consulta de bajo mínimo.
- Gestión de compras a proveedor con detalle de ítems.
- Gestión de facturas con detalle de ítems.
- Gestión de usuarios, empleados y roles.
- Flujo de autenticación con token JWT.

La aplicación expone documentación interactiva en Swagger y ReDoc, y además integra un menú CLI que consume la API para escenarios de operación rápida.

## Arquitectura del proyecto

La solución está organizada por capas:

- Presentación HTTP: rutas FastAPI en src/api.
- Validación y contratos: modelos Pydantic en src/models.py.
- Lógica de negocio y acceso a datos: clases CRUD en src/crud.
- Persistencia: entidades ORM en src/entities.
- Núcleo transversal: configuración, auth, respuestas y manejo global de errores en src/core.
- Datos iniciales e infraestructura de esquema: migraciones y seeders en src/migrations y src/database.

Este diseño separa responsabilidades y facilita mantenimiento, pruebas y evolución de esquema.

## Estructura de carpetas

```text
superMarketBackEnd/
  .github/workflows/
    ci.yml                    # Validación continua en DEV
    cd.yml                    # Build y publicación de imagen en GHCR
  alembic.ini                 # Configuración de Alembic
  bootstrap_db.py             # Migraciones + seeders
  migrate_db.py               # Solo migraciones
  seed_db.py                  # Solo seeders
  Dockerfile                  # Imagen para despliegue
  requirements.txt
  src/
    api/                      # Routers FastAPI por dominio
    core/                     # Configuración, auth, errores y respuestas
    crud/                     # Servicios CRUD
    database/                 # Bootstrap y seeders
    entities/                 # Modelos ORM SQLAlchemy
    migrations/               # Entorno y versiones Alembic
    main.py                   # App FastAPI + registro de routers
    menu.py                   # Menú de consola (cliente HTTP interno)
    models.py                 # Esquemas Pydantic
  tests/
    test_smoke.py
```

## Stack tecnológico

- FastAPI y Uvicorn
- SQLAlchemy 2.x
- Alembic
- PostgreSQL (driver psycopg2-binary)
- Pydantic v2
- JWT con PyJWT
- Bcrypt para hash de contraseñas
- Requests y HTTPX
- Pytest

## Módulos funcionales

- Auth: login y usuario autenticado actual.
- Usuarios y Empleados: gestión de cuentas, perfiles operativos y estado.
- Clientes y Proveedores: maestros de terceros.
- Productos y Tipos: catálogo de productos.
- Sucursales: puntos de operación.
- Inventario: existencias por producto/sucursal y ajustes de stock.
- Compras a proveedor: cabecera y detalle con soporte de anulación.
- Facturación: cabecera y detalle con soporte de anulación.
- Roles: control de perfiles y salario base asociado.

## Mapa de endpoints

Todos los prefijos, salvo /auth, requieren usuario autenticado y activo.

### Auth

- POST /auth/login
- GET /auth/me

### Usuarios

- POST /usuarios/
- GET /usuarios/
- GET /usuarios/{usuario_id}
- PUT /usuarios/{usuario_id}
- DELETE /usuarios/{usuario_id}

### Empleados

- POST /empleados/
- GET /empleados/
- GET /empleados/{empleado_id}
- PUT /empleados/{empleado_id}
- DELETE /empleados/{empleado_id}

### Clientes

- POST /clientes/
- GET /clientes/
- GET /clientes/{cliente_id}
- PUT /clientes/{cliente_id}
- DELETE /clientes/{cliente_id}

### Proveedores

- POST /proveedores/
- GET /proveedores/
- GET /proveedores/{proveedor_id}
- PUT /proveedores/{proveedor_id}
- DELETE /proveedores/{proveedor_id}

### Productos

- POST /productos/
- GET /productos/
- GET /productos/{producto_id}
- PUT /productos/{producto_id}
- DELETE /productos/{producto_id}

### Tipos de producto

- POST /tipos-producto/
- GET /tipos-producto/
- GET /tipos-producto/{tipo_id}
- PUT /tipos-producto/{tipo_id}
- DELETE /tipos-producto/{tipo_id}

### Sucursales

- POST /sucursales/
- GET /sucursales/
- GET /sucursales/{sucursal_id}
- PUT /sucursales/{sucursal_id}
- DELETE /sucursales/{sucursal_id}

### Inventario

- POST /inventarios/
- GET /inventarios/
- GET /inventarios/bajo-minimo
- GET /inventarios/sucursal/{sucursal_id}
- GET /inventarios/{inventario_id}
- PUT /inventarios/{inventario_id}
- PATCH /inventarios/{inventario_id}/ajustar-stock
- DELETE /inventarios/{inventario_id}

### Compras a proveedor

- POST /compras-proveedor/
- GET /compras-proveedor/
- GET /compras-proveedor/proveedor/{proveedor_id}
- GET /compras-proveedor/{compra_id}
- PUT /compras-proveedor/{compra_id}
- PATCH /compras-proveedor/{compra_id}/anular
- POST /compras-proveedor/{compra_id}/detalles
- GET /compras-proveedor/{compra_id}/detalles
- GET /compras-proveedor/detalles/{detalle_id}
- DELETE /compras-proveedor/detalles/{detalle_id}

### Facturas

- POST /facturas/
- GET /facturas/
- GET /facturas/cliente/{cliente_id}
- GET /facturas/sucursal/{sucursal_id}
- GET /facturas/{factura_id}
- PUT /facturas/{factura_id}
- PATCH /facturas/{factura_id}/anular
- GET /facturas/{factura_id}/detalles
- GET /facturas/detalles/{detalle_id}
- DELETE /facturas/detalles/{detalle_id}

### Roles

- POST /roles/
- GET /roles/
- GET /roles/{rol_id}
- PUT /roles/{rol_id}
- DELETE /roles/{rol_id}

## Autenticación y autorización

### Login

Endpoint: POST /auth/login

El endpoint acepta dos formatos:

- JSON (útil para clientes propios):

```json
{
  "username": "admin",
  "password": "admin123"
}
```

- Formulario application/x-www-form-urlencoded (compatible con el modal Authorize de Swagger).

Respuesta esperada:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Uso del token

Enviar cabecera Authorization en endpoints protegidos:

```http
Authorization: Bearer <access_token>
```

Validación rápida de sesión:

- GET /auth/me

## Variables de entorno

Se recomienda un archivo .env en la raíz.

| Variable               | Requerida | Valor por defecto                             | Descripción                                                     |
| ---------------------- | --------- | --------------------------------------------- | --------------------------------------------------------------- |
| DATABASE_URL           | Sí        | N/A                                           | Cadena de conexión SQLAlchemy a PostgreSQL.                     |
| SSL_MODE               | No        | require                                       | sslmode para conexiones PostgreSQL. En local suele ser disable. |
| JWT_SECRET_KEY         | No        | dev-only-change-this-secret-at-least-32-bytes | Clave de firma JWT. Debe cambiarse en producción.               |
| JWT_ALGORITHM          | No        | HS256                                         | Algoritmo de firma JWT.                                         |
| JWT_EXPIRE_MINUTES     | No        | 60                                            | Minutos de vida del token.                                      |
| CORS_ALLOW_ORIGINS     | No        | http://localhost:4200,http://127.0.0.1:4200   | Lista de orígenes separados por coma. En produccion debe incluir https://santi-osp.github.io. |
| CORS_ALLOW_CREDENTIALS | No        | true                                          | Habilita credenciales en CORS.                                  |
| RUN_SEEDERS_ON_STARTUP | No        | false                                         | Ejecuta seeders al levantar la API.                             |
| HTTP_CLIENT_BASE_URL   | No        | http://localhost:8000                         | URL base usada por menu.py.                                     |

Ejemplo mínimo para desarrollo local:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/supermarket
SSL_MODE=disable
JWT_SECRET_KEY=super-secret-change-me-32chars-min
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
CORS_ALLOW_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
CORS_ALLOW_CREDENTIALS=true
RUN_SEEDERS_ON_STARTUP=false
HTTP_CLIENT_BASE_URL=http://localhost:8000
```

Ejemplo para permitir el frontend local y el despliegue en GitHub Pages:

```env
CORS_ALLOW_ORIGINS=http://localhost:4200,http://127.0.0.1:4200,https://santi-osp.github.io
```

## Instalación y ejecución local

### 1) Crear entorno e instalar dependencias

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Inicializar base de datos

Opción recomendada (todo en uno):

```bash
python bootstrap_db.py
```

Opción por pasos:

```bash
python migrate_db.py
python seed_db.py
```

### 3) Levantar API

Desde raíz del repositorio:

```bash
uvicorn main:app --app-dir src --reload
```

URLs:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Migraciones y seeders

### Scripts disponibles

- python migrate_db.py: aplica migraciones pendientes hasta head.
- python seed_db.py: ejecuta seeders idempotentes.
- python bootstrap_db.py: ejecuta migraciones y luego seeders.

### Qué siembran los seeders

- Roles base: admin, gerente, empleado.
- Usuario administrador inicial: admin / admin123.
- Catálogo de sucursales, tipos de producto, proveedores y productos.
- Datos iniciales de clientes y empleados.

### Características del seeding

- Idempotente: evita duplicados por claves de negocio.
- Compatible con reejecuciones sucesivas.
- Mantiene auditoría de creación cuando aplica.

## Uso del menú de consola

El menú está en src/menu.py y consume la API por HTTP.

Ejecutar:

```bash
python src/main.py
```

Opciones principales del menú:

- 1 a 11: módulos de negocio (clientes, productos, proveedores, sucursales, tipos, usuarios, empleados, inventario, compras, facturas y roles).
- 12: iniciar servidor FastAPI local desde el menú.

Nota: para usar opciones de negocio, la API debe estar levantada y accesible en HTTP_CLIENT_BASE_URL.

## Ejecución con Docker

Construir imagen:

```bash
docker build -t supermarket-backend .
```

Ejecutar contenedor:

```bash
docker run --rm -p 8000:8000 --env-file .env supermarket-backend
```

La imagen expone el puerto 8000 y levanta uvicorn con main:app desde /app/src.

## Pruebas, lint y seguridad

Pruebas:

```bash
pytest -q
```

Lint y formato (si tienes Ruff instalado):

```bash
ruff check src --output-format=github
ruff format src --check
```

Auditoría de dependencias:

```bash
pip-audit -r requirements.txt
```

## CI/CD

### CI (archivo .github/workflows/ci.yml)

Se ejecuta en push y pull_request hacia rama DEV.

Incluye:

- Servicio PostgreSQL 15 en GitHub Actions.
- Instalación de dependencias.
- Bootstrap de base de datos.
- Verificación de seed de roles base.
- Lint y formato con Ruff.
- Auditoría de dependencias con pip-audit.
- Pruebas con pytest.

### CD (archivo .github/workflows/cd.yml)

Se activa por workflow_run cuando CI finaliza con éxito.

Acciones:

- Build de imagen Docker.
- Login a GHCR.
- Publicación de imagen en ghcr.io con tags por SHA y rama.

## Despliegue en Render

El backend esta desplegado publicamente en Render:

```text
https://supermarketbackend.onrender.com
```

Rutas utiles en produccion:

- API raiz: https://supermarketbackend.onrender.com
- Swagger: https://supermarketbackend.onrender.com/docs
- ReDoc: https://supermarketbackend.onrender.com/redoc

Variables que deben estar configuradas en Render:

- DATABASE_URL
- SSL_MODE=require
- JWT_SECRET_KEY
- JWT_ALGORITHM=HS256
- JWT_EXPIRE_MINUTES=60
- CORS_ALLOW_ORIGINS=https://santi-osp.github.io
- CORS_ALLOW_CREDENTIALS=true
- RUN_SEEDERS_ON_STARTUP=false

El frontend desplegado en GitHub Pages consume esta URL de API:

```text
https://supermarketbackend.onrender.com
```

## Troubleshooting

### Error al iniciar por DATABASE_URL

Síntoma:

- ValueError indicando que falta DATABASE_URL.

Solución:

- Definir DATABASE_URL en .env o en variables de entorno del sistema.

### Conexión SSL en local falla

Síntoma:

- Error de conexión PostgreSQL por sslmode.

Solución:

- En entorno local usar SSL_MODE=disable.

### 401 en endpoints protegidos

Síntoma:

- Acceso denegado en rutas distintas de /auth.

Solución:

- Hacer login en /auth/login y enviar Authorization: Bearer <token>.

### Authorize de Swagger no autentica

Estado actual:

- /auth/login acepta formulario OAuth2 y JSON, por lo que el modal Authorize es compatible.

### Menú no conecta con la API

Síntoma:

- Mensaje de error de conexión en el menú.

Solución:

- Levantar servidor con opción 12 del menú o ejecutar uvicorn manualmente.
- Verificar HTTP_CLIENT_BASE_URL.

## Buenas prácticas operativas

- Cambiar JWT_SECRET_KEY en cualquier entorno no local.
- Cambiar credenciales de admin por defecto después del primer seed.
- Mantener esquema exclusivamente con Alembic (no cambios manuales en BD productiva).
- Mantener seeders idempotentes y orientados a claves de negocio.
