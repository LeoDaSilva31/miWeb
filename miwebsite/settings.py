# miwebsite/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Seguridad / debug ---
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# Render te asigna un dominio *.onrender.com


ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'miweb-6ixr.onrender.com',
                 'leods-blog.org', 'www.leods-blog.org', '.onrender.com']



render_external_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if render_external_hostname:
    ALLOWED_HOSTS.append(render_external_hostname)
# También podés permitir explícitamente el wildcard de Render si querés:
ALLOWED_HOSTS += ['.onrender.com']

# --- Apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bienvenida',  # App principal del sitio
    'catalogo',    # App de productos/catálogo
    'storages',
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise para servir estáticos en producción
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'miwebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # templates dentro de cada app
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'miwebsite.wsgi.application'

# --- Base de datos ---
# Por defecto preparamos PostgreSQL para desarrollo local.
# Se puede configurar con la variable de entorno DATABASE_URL o con las variables
# DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.
if os.getenv('DATABASE_URL'):
    # dj-database-url permite parsear DATABASE_URL (opcional)
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
        }
    except Exception:
        # Si no está dj-database-url disponible, caemos a la configuración por partes
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('DB_NAME', 'miweb'),
                'USER': os.getenv('DB_USER', 'miweb'),
                'PASSWORD': os.getenv('DB_PASSWORD', 'miweb'),
                'HOST': os.getenv('DB_HOST', 'localhost'),
                'PORT': os.getenv('DB_PORT', '5432'),
            }
        }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'miweb'),
            'USER': os.getenv('DB_USER', 'miweb'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'miweb'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

# --- Password validators ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internacionalización ---
# Para Argentina te conviene:
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # donde collectstatic deposita


import os  # Esto ya lo tenés arriba

# ==========================
# MinIO / S3-compatible media storage
# ==========================
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'http://127.0.0.1:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'django-media')
MINIO_USE_SSL = os.getenv('MINIO_USE_SSL', 'False').lower() == 'true'


AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT
AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET

# MinIO no necesita región real
AWS_S3_REGION_NAME = None

# Para MinIO: URLs tipo http://127.0.0.1:9000/bucket/archivo
AWS_S3_ADDRESSING_STYLE = 'path'

# Recomendado en versiones nuevas de django-storages
AWS_DEFAULT_ACL = None

AWS_S3_USE_SSL = MINIO_USE_SSL
AWS_S3_VERIFY = False  # en local, sin HTTPS real, mejor desactivar

# Control de firma (querystring) para URLs prefirmadas.
# Opción B: permitir desactivar firmas en local mediante la variable de entorno
# AWS_QUERYSTRING_AUTH=False en tu .env local. En producción dejar True para
# URLs firmadas y expirables.
AWS_QUERYSTRING_AUTH = os.getenv('AWS_QUERYSTRING_AUTH', 'True').lower() in ('true', '1', 't')


# ==========================
# STORAGES - Django 5.x
# ==========================

# STORAGES: usar S3Boto3Storage para media y WhiteNoise para estáticos.
# En este proyecto se fuerza el uso de MinIO/S3 para todos los entornos.
STORAGES = {
    # Storage por defecto para archivos de usuario (ImageField, FileField, etc.)
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    # Storage para archivos estáticos (WhiteNoise)
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Forzamos S3/MinIO como storage por defecto (si las credenciales no existen,
# la configuración fallará al inicializar; el flujo de trabajo del proyecto
# siempre debe usar MinIO y PostgreSQL).
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# --- Archivos multimedia ---
# Este proyecto usa MinIO/S3 para media; eliminamos el uso de un directorio
# local (`MEDIA_ROOT`). Dejamos `MEDIA_URL` vacío para evitar referencias a
# rutas locales en plantillas o configuración.
MEDIA_URL = ''

# ==========================
# Límites de tamaño de subida (3 MB)
# ==========================

# Tamaño máximo del cuerpo completo de la request (3 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 3 * 1024 * 1024  # 3 MiB

# Tamaño máximo de un archivo individual en memoria (3 MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 3 * 1024 * 1024  # 3 MiB


# --- Cabeceras seguras detrás de proxy ---
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- CSRF (necesario en Render) ---
# CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://leods-blog.org',
    'https://www.leods-blog.org',
]

# --- Default PK ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ya no se utiliza Supabase en este proyecto. Configure PostgreSQL usando las
# variables de entorno: DATABASE_URL ó DB_NAME/DB_USER/DB_PASSWORD/DB_HOST/DB_PORT.
