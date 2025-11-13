# Leo Da Silva - Portafolio Web

Sitio web profesional de desarrollador con aplicaciones demo construido con Django, optimizado para SEO y diseño responsive.

## 🚀 Características

- ✅ **Página principal** con información profesional
- ✅ **Demo Panadería** - Landing page comercial responsive
- ✅ **Sistema Directorio** - App con búsqueda en tiempo real
- ✅ **SEO optimizado** - Meta tags, sitemap, schema.org
- ✅ **Diseño responsive** - Optimizado para móviles
- ✅ **Base de datos** - Gestión de contactos con Django ORM

## 🛠️ Instalación Local

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/LeoDaSilva31/miWeb.git
   cd miWeb
   ```

2. **Crear y activar entorno virtual**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate    # Linux/Mac
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar PostgreSQL (y opcionalmente pgAdmin) y crear la base de datos local**:

   - Instala PostgreSQL en tu máquina (Windows: instalador oficial, Linux: apt/yum, Mac: Homebrew).
   - Abre pgAdmin o psql y crea una base de datos y un usuario. Ejemplo:

     ```sql
     CREATE USER miweb WITH PASSWORD 'miweb';
     CREATE DATABASE miweb OWNER miweb;
     ```

   - Alternativamente, usa `pgAdmin` para crear la base y el usuario.

5. **Configurar variables de entorno**:

   - Copia `.env.example` a `.env` y ajusta los valores (SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, etc.).
   - El proyecto usa `python-dotenv` para cargar `.env` en `settings.py`.

6. **Ejecutar migraciones**:

   ```bash
   python manage.py migrate
   ```

7. **Cargar datos de ejemplo (opcional)**:

   ```bash
   python manage.py cargar_datos_ejemplo
   ```

8. **Ejecutar servidor**:
   ```bash
   python manage.py runserver
   ```
   Visita: http://127.0.0.1:8000

## 🎯 Aplicaciones Demo

### 🏪 Panadería (Landing Page)

- **URL**: `/panaderia/`
- **Características**: Diseño comercial, responsive, demo funcional
- **Tecnologías**: Django, Tailwind CSS, JavaScript

### 👥 Sistema Directorio

- **URL**: `/directorio/`
- **Características**: Búsqueda en tiempo real, AJAX, base de datos
- **Tecnologías**: Django ORM, SQLite, JSON responses

## 📁 Estructura del Proyecto

```
miWeb/
├── bienvenida/           # App principal
├── panaderia/           # Demo landing page comercial
├── directorio/          # Demo sistema directorio
│   ├── models.py        # Modelo Socio
│   ├── views.py         # Vistas y búsqueda AJAX
│   ├── management/commands/  # Comando cargar datos
│   └── templates/       # Templates responsive
├── miwebsite/           # Configuración Django
├── sitemap.xml          # SEO sitemap
├── robots.txt           # SEO robots
├── requirements.txt     # Dependencias
└── README.md           # Documentación
```

## 🔧 Comandos Útiles

```bash
# Servidor de desarrollo
python manage.py runserver

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Cargar datos demo directorio
python manage.py cargar_datos_ejemplo

# Admin (crear superuser)
python manage.py createsuperuser
```

## � SEO Implementado

- ✅ Meta tags optimizados con keywords
- ✅ Open Graph y Twitter Cards
- ✅ Schema.org structured data
- ✅ Sitemap.xml automático
- ✅ Robots.txt configurado
- ✅ URLs canónicas

## 🎨 Tecnologías

- **Backend**: Django 5.2.7, Python 3.13
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Base de Datos**: SQLite (desarrollo)
- **SEO**: Meta tags, Schema.org, Sitemap
- **Deploy**: Whitenoise, Gunicorn

## 🌐 En Producción

- **URL**: https://leods-blog.org
- **Hosting**: Render
- **Dominio**: Configurado con DNS

## 📧 Contacto

**Leo Da Silva** - Desarrollador Web

- GitHub: [@LeoDaSilva31](https://github.com/LeoDaSilva31)
- Web: https://leods-blog.org

---

Desarrollado con ❤️ usando Django | Portfolio profesional 2025
