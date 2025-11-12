# 🚀 Configuración de Supabase

Este documento te guía para configurar Supabase como base de datos y storage para el proyecto.

## 📋 Pasos para configurar

### 1. Configurar variables de entorno

Edita el archivo `.env` y reemplaza las siguientes variables con tus credenciales de Supabase:

```bash
# Configuración de Supabase
SUPABASE_URL=tu_supabase_url_aqui
SUPABASE_KEY=tu_supabase_anon_key_aqui
SUPABASE_SERVICE_KEY=tu_supabase_service_key_aqui

# Configuración de Storage (Buckets)
SUPABASE_BUCKET_NAME=productos-images
```

### 2. Obtener las credenciales

Desde tu proyecto en Supabase (https://app.supabase.com):

1. **SUPABASE_URL**: Ve a Settings > API > Project URL
2. **SUPABASE_KEY**: Ve a Settings > API > Project API keys > anon public
3. **SUPABASE_SERVICE_KEY**: Ve a Settings > API > Project API keys > service_role (¡mantén esta clave segura!)

### 3. Probar la conexión

Una vez que hayas configurado las credenciales:

```bash
python manage.py test_supabase
```

### 4. Ejecutar migraciones

Si la conexión es exitosa, ejecuta las migraciones:

```bash
python manage.py migrate_supabase
```

## 🛠️ Lo que se configurará

### Tabla `productos`

- `id` (UUID, primary key)
- `titulo` (VARCHAR(255))
- `descripcion` (TEXT)
- `precio` (DECIMAL(10,2))
- `foto_url` (TEXT)
- `activo` (BOOLEAN)
- `orden` (INTEGER)
- `fecha_creacion` (TIMESTAMP)
- `fecha_actualizacion` (TIMESTAMP)

### Bucket de Storage

- Nombre: `productos-images`
- Acceso público para lectura
- Políticas de seguridad configuradas

### Características incluidas

- ✅ Row Level Security (RLS)
- ✅ Triggers automáticos para timestamps
- ✅ Índices para optimizar consultas
- ✅ Políticas de acceso configuradas
- ✅ Storage bucket para imágenes

## 🔧 Comandos disponibles

```bash
# Probar conexión
python manage.py test_supabase

# Ejecutar migraciones
python manage.py migrate_supabase

# Ejecutar migraciones usando script directo
python scripts/migrate_supabase.py

# Probar conexión usando script directo
python scripts/test_supabase.py
```

## 📁 Archivos creados

- `miwebsite/supabase_config.py` - Configuración y utilidades de Supabase
- `catalogo/supabase_models.py` - Modelos para trabajar con Supabase
- `scripts/migrate_supabase.py` - Script de migración
- `scripts/test_supabase.py` - Script de prueba de conexión
- Comandos de Django en `catalogo/management/commands/`

## 🎯 Próximos pasos

Después de configurar Supabase exitosamente:

1. Las vistas pueden usar tanto Django ORM como Supabase
2. Los modelos de Supabase tienen métodos como `.all()`, `.filter()`, `.save()`, `.delete()`
3. Las imágenes se pueden subir al bucket usando `upload_image_to_bucket()`
4. Se puede migrar gradualmente desde SQLite a Supabase

## ⚠️ Importante

- **NO** subas el archivo `.env` al repositorio
- Mantén la `SERVICE_KEY` segura
- Usa la `ANON_KEY` para operaciones públicas
- Usa la `SERVICE_KEY` solo para operaciones administrativas
