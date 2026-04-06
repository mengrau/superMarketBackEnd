# 📊 Guía de Implementación de Seeders

He creado un sistema completo de seeders para tu base de datos SuperMarket. Aquí está todo lo que necesitas saber.

## 📁 Archivos Creados

### 1. **`src/database/seeders.py`** (Principal)
Script que contiene toda la lógica para crear datos de prueba:
- Roles
- Usuario administrador
- Sucursales
- Tipos de productos
- Proveedores
- Productos
- Clientes
- Empleados

### 2. **`cli.py`** (En la raíz del proyecto)
Interfaz de línea de comandos para ejecutar los seeders fácilmente.

### 3. **`src/database/seeder_config.py`**
Configuración que lee variables de entorno para habilitar seeders automáticos en el startup.

### 4. **`src/database/__main__.py`**
Permite ejecutar los seeders como módulo de Python.

### 5. **`src/database/SEEDERS.md`**
Documentación detallada del sistema de seeders.

### 6. **`src/main.py`** (Modificado)
Se agregó soporte para ejecutar seeders automáticamente al startup (opcional).

## 🚀 Cómo Usar

### Opción 1: Usando el CLI (⭐ Recomendado)
```bash
python cli.py seed
```

### Opción 2: Comando de Python
```bash
python -m src.database.seeders
```

### Opción 3: Ejecutar automáticamente al startup
Agrega esto a tu archivo `.env`:
```env
RUN_SEEDERS_ON_STARTUP=true
```

Luego, cuando inicies la API, los seeders se ejecutarán automáticamente.

### Opción 4: Desde código Python
```python
from src.database.seeders import seed_database

seed_database()
```

## 📊 Datos que se Crean

| Elemento | Cantidad | Detalles |
|----------|----------|---------|
| **Roles** | 4 | Administrador, Gerente, Empleado, Analista |
| **Usuarios** | 4 | 1 admin + 3 empleados |
| **Sucursales** | 3 | Centro, Norte, Sur |
| **Tipos de Producto** | 8 | Alimentos, Bebidas, Lácteos, etc. |
| **Proveedores** | 3 | Distribuidoras y importadores |
| **Productos** | 12 | Leche, Pan, Pollo, Frutas, etc. |
| **Clientes** | 4 | Clientes de prueba con datos realistas |
| **Empleados** | 3 | Cajero, Reponedor, Gerente |

## 🔐 Credenciales de Prueba

```
Usuario: admin
Contraseña: admin123
Rol: Administrador

Empleados:
- Usuario: carlos.mendoza | Contraseña: empleado123 | Rol: Empleado
- Usuario: diana.torres | Contraseña: empleado123 | Rol: Empleado
- Usuario: felipe.ramirez | Contraseña: empleado123 | Rol: Gerente
```

## ✨ Características del Sistema

### ✅ Idempotente
Puedes ejecutar los seeders múltiples veces sin crear duplicados. El script verifica si los datos ya existen.

### ✅ Transaccional
Si ocurre un error, todos los cambios se revierten automáticamente.

### ✅ Informativo
Muestra el progreso y un resumen final de los datos creados.

### ✅ Auditable
Todos los registros tienen:
- `id_usuario_creacion`: Quién creó el registro (admin)
- `fecha_creacion`: Cuándo se creó
- `estado`: Siempre `True` (activo) para datos iniciales

## 📋 Salida Esperada

Cuando ejecutes los seeders, verás algo como esto:

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
  ... (más información)

============================================================
✓ SEEDERS COMPLETADOS EXITOSAMENTE
============================================================

📊 Resumen:
  • Roles: 4
  • Usuarios: 4
  • Sucursales: 3
  • Tipos de Producto: 8
  • Productos: 12
  • Proveedores: 3
  • Clientes: 4
  • Empleados: 3
```

## 🛡️ Seguridad y Mejores Prácticas

### ⚠️ Importante
1. **NO ejecutes seeders en producción** automáticamente (RUN_SEEDERS_ON_STARTUP=false)
2. **Cambia las contraseñas** después de usar los datos de prueba
3. Los seeders solo funcionan si tienes conexión a la base de datos configurada
4. Se recomienda ejecutar seeders solo en ambiente de desarrollo

### 🔄 Flujo Recomendado en Desarrollo

1. Crear las tablas:
   ```bash
   python -c "from src.database.config import create_tables; create_tables()"
   ```

2. Ejecutar los seeders:
   ```bash
   python cli.py seed
   ```

3. (Opcional) Ejecutar migraciones Alembic si es necesario:
   ```bash
   alembic upgrade head
   ```

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'src'"
Ejecuta los comandos desde la raíz del proyecto:
```bash
cd c:\Users\emman\superMarketBackEnd
python cli.py seed
```

### Error: "DATABASE_URL not set"
Asegúrate de tener un archivo `.env` con:
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost/supermarket
```

### Error: "Table already exists"
Es normal si ya tienes datos. Los seeders verificarán si existen y no crearán duplicados.

## 📝 Personalización

Si quieres agregar más datos, edita `src/database/seeders.py`:

1. Abre el archivo
2. Encuentra la función correspondiente (ej: `crear_productos`)
3. Agrega más elementos a `___data`
4. Ejecuta nuevamente

Ejemplo:
```python
def crear_productos(...):
    productos_data = [
        {
            "nombre": "Mi Nuevo Producto",
            "tipo_idx": 0,
            "proveedor_idx": 0,
            "precio": Decimal("5.99"),
            "codigo_barras": "1234567890123",
        },
        # ... más productos
    ]
```

## 📞 Soporte

Si tienes problemas:
1. Verifica que tu BD esté corriendo
2. Revisa los logs del error específico
3. Asegúrate de que las entidades estén actualizadas
4. Los seeders usan los mismos modelos que tu API

¡Que disfrutes!
