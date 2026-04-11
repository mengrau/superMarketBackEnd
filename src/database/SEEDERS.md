# Seeders de Base de Datos

Este módulo contiene scripts para popular la base de datos con datos de prueba automáticamente.

## ¿Qué son los Seeders?

Los seeders son scripts que crean datos iniciales en la base de datos cuando se ejecutan. Son útiles para:
- Crear datos de prueba para desarrollo
- Inicializar la BD con datos básicos obligatorios (ej: roles)
- Testing automatizado
- Reproducibilidad en diferentes ambientes

## Datos que se crean

Al ejecutar los seeders, se crean automáticamente:

### 1. **Roles (4)**
   - Administrador (salario: $3000)
   - Gerente (salario: $2500)
   - Empleado (salario: $1200)
   - Analista (salario: $1500)

### 2. **Usuario Administrador**
   - Usuario: `admin`
   - Contraseña: `admin123`

### 3. **Sucursales (3)**
   - SuperMarket Centro
   - SuperMarket Norte
   - SuperMarket Sur

### 4. **Tipos de Productos (8)**
   - Alimentos
   - Bebidas
   - Lácteos
   - Carnes y Pescados
   - Frutas y Verduras
   - Productos de Limpieza
   - Higiene Personal
   - Productos Congelados

### 5. **Proveedores (3)**
   - Distribuidora Nacional
   - Importaciones Rápidas
   - Productos Frescos SA

### 6. **Productos (12)**
   - Leche Entera, Queso, Yogurt
   - Pan Integral
   - Pollo Fresco, Atún
   - Manzanas, Lechuga
   - Detergente, Jabón
   - Agua, Refresco

### 7. **Clientes (4)**
   - Juan Carlos García
   - María Elena López
   - Roberto Díaz Martín
   - Ana Rodríguez Pérez

### 8. **Empleados (3)**
   - Carlos Mendoza (Cajero)
   - Diana Torres (Reponedor)
   - Felipe Ramírez (Gerente de Turno)

## Cómo usar

### Opción 1: Usando el CLI (Recomendado)

```bash
python cli.py seed
```

### Opción 2: Ejecutar como módulo Python

```bash
python -m src.database.seeders
```

### Opción 3: Importar en código

```python
from src.database.seeders import seed_database

seed_database()
```

## Características

✅ **Idempotente**: Los seeders verifican si los datos ya existen antes de crearlos, por lo que se pueden ejecutar múltiples veces sin crear duplicados.

✅ **Transaccional**: Si algo sale mal, los cambios se revierten automáticamente.

✅ **Informativo**: Muestra el progreso y resumen de datos creados.

## Salida esperada

```
============================================================
INICIANDO SEEDERS DE BASE DE DATOS
============================================================

1. Creando Roles...
  ✓ Rol 'Administrador' creado
  ✓ Rol 'Gerente' creado
  ✓ Rol 'Empleado' creado
  ✓ Rol 'Analista' creado

2. Creando Usuario Administrador...
  ✓ Usuario 'admin' creado (contraseña: admin123)

3. Creando Sucursales...
  ✓ Sucursal 'SuperMarket Centro' creada
  ✓ Sucursal 'SuperMarket Norte' creada
  ✓ Sucursal 'SuperMarket Sur' creada

... (más datos)

============================================================
✓ SEEDERS COMPLETADOS EXITOSAMENTE
============================================================

📊 Resumen:
  • Roles: 4
  • Usuarios: 4 (admin + empleados)
  • Sucursales: 3
  • Tipos de Producto: 8
  • Productos: 12
  • Proveedores: 3
  • Clientes: 4
  • Empleados: 3

🔑 Credenciales por defecto:
  • Usuario admin: admin / admin123
  • Empleados: {username} / empleado123
```

## Credenciales de prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | admin123 | Administrador |
| carlos.mendoza | empleado123 | Empleado |
| diana.torres | empleado123 | Empleado |
| felipe.ramirez | empleado123 | Gerente |

## Notas

- Los seeders solo crean datos que no existan previamente
- Si ejecutas los seeders nuevamente, solo se crearán los datos nuevos
- Los datos creados por los seeders tienen marcas de auditoría (id_usuario_creacion, fecha_creacion)
- Todos los datos se marcan como estado `activo = True`

## Permisos y auditoría

- Todos los registros creados tienen `id_usuario_creacion` apuntando al usuario admin
- Esto permite rastrear quién creó los datos iniciales
- Los timestamps se registran automáticamente con la zona horaria UTC
