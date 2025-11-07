# Mi Sitio Web - Django

Un sitio web sencillo construido con Django, con una página de bienvenida "Sitio en construcción".

## 🚀 Características

- ✅ Página de bienvenida "Sitio en construcción" moderna y responsiva
- ✅ App Django organizada (`bienvenida`)
- ✅ Diseño con gradientes y animaciones CSS
- ✅ Configuración con variables de entorno
- ✅ Responsive design

## 🛠️ Instalación Local

1. **Clonar el repositorio**:

   ```bash
   git clone <tu-repositorio>
   cd miWeb
   ```

2. **Crear y activar entorno virtual**:

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   # source .venv/bin/activate    # Linux/Mac
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:

   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones si es necesario
   ```

5. **Ejecutar migraciones**:

   ```bash
   python manage.py migrate
   ```

6. **Ejecutar el servidor de desarrollo**:

   ```bash
   python manage.py runserver
   ```

   Visita: http://127.0.0.1:8000

## 📁 Estructura del proyecto

```
miWeb/
├── .venv/                 # Entorno virtual
├── bienvenida/            # App de Django para página de bienvenida
│   ├── static/bienvenida/css/  # Estilos CSS
│   ├── templates/bienvenida/   # Templates HTML
│   ├── views.py          # Vistas
│   ├── urls.py           # URLs de la app
│   └── ...
├── miwebsite/             # Configuración principal de Django
│   ├── settings.py       # Configuración del proyecto
│   ├── urls.py           # URLs principales
│   └── ...
├── manage.py             # Herramienta de gestión de Django
├── requirements.txt      # Dependencias de Python
├── .env.example         # Ejemplo de variables de entorno
├── .gitignore          # Archivos ignorados por Git
└── README.md          # Este archivo
```

## 🎨 Personalización

### Cambiar el contenido

Edita `bienvenida/templates/bienvenida/index.html` para modificar:

- Título principal
- Descripción
- Enlaces de redes sociales
- Información de contacto
- Porcentaje de progreso

### Cambiar los estilos

Edita `bienvenida/static/bienvenida/css/style.css` para modificar:

- Colores y gradientes
- Tipografías
- Animaciones
- Diseño responsivo

## 🔧 Comandos útiles

```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (para admin)
python manage.py createsuperuser
```

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

Desarrollado con ❤️ usando Django
