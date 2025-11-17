# miwebsite/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Seguridad / debug ---
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# --- Hosts permitidos ---
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'miweb-6ixr.onrender.com',
    'leods-blog.org',
    'www.leods-blog.org',
    '.onrender.com',
]

render_external_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if render_external_hostname:
    ALLOWED_HOSTS.append(render_external_hostname)

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
    # 'storages',  # <- ya no lo necesitamos para MinIO/S3
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
# Usamos DATABASE_URL si existe (Render o tu .env local con la URL externa de Render).
# Si no, caemos a configuración manual con variables DB_*.
if os.getenv('DATABASE_URL'):
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
        }
    except Exception:
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
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # donde collectstatic deposita

# ==========================
#  STORAGE (MEDIA + STATIC)
# ==========================
# Sin MinIO / S3. Usamos disco local para media y WhiteNoise para estáticos.

STORAGES = {
    # Archivos subidos por usuarios (ImageField, FileField, etc.)
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # Archivos estáticos (CSS, JS, imágenes de static/) servidos por WhiteNoise
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Archivos multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================
# Límites de tamaño de subida (3 MB)
# ==========================

DATA_UPLOAD_MAX_MEMORY_SIZE = 3 * 1024 * 1024  # 3 MiB
FILE_UPLOAD_MAX_MEMORY_SIZE = 3 * 1024 * 1024  # 3 MiB

# --- Cabeceras seguras detrás de proxy ---
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- CSRF (necesario en Render) ---
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://leods-blog.org',
    'https://www.leods-blog.org',
]

# --- Default PK ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
