"""
Script para crear productos de prueba en Supabase
"""
import sys
import os
sys.path.append('D:/miWeb')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
import django
django.setup()

from catalogo.supabase_models import ProductoSupabase

def crear_productos_prueba():
    """
    Crea algunos productos de prueba en Supabase
    """
    print("🧪 Creando productos de prueba en Supabase...")
    
    productos_prueba = [
        {
            'titulo': 'Página Web Profesional',
            'descripcion': 'Desarrollo de sitio web responsive y optimizado para SEO. Incluye diseño moderno, adaptado a móviles y optimización para motores de búsqueda.',
            'precio': 299.99,
            'activo': True,
            'orden': 1
        },
        {
            'titulo': 'Aplicación Web Django',
            'descripcion': 'Sistema web completo desarrollado con Django. Incluye panel administrativo, base de datos y funcionalidades personalizadas según tus necesidades.',
            'precio': 799.99,
            'activo': True,
            'orden': 2
        },
        {
            'titulo': 'E-commerce Completo',
            'descripcion': 'Tienda online profesional con carrito de compras, pasarela de pagos y panel de administración. Ideal para vender productos o servicios online.',
            'precio': 1299.99,
            'activo': True,
            'orden': 3
        },
        {
            'titulo': 'Landing Page',
            'descripcion': 'Página de aterrizaje optimizada para conversiones. Diseño atractivo y enfocado en generar leads o ventas para tu negocio.',
            'precio': 149.99,
            'activo': True,
            'orden': 4
        },
        {
            'titulo': 'Consultoría Web',
            'descripcion': 'Asesoría personalizada para mejorar tu presencia digital. Análisis de sitio actual y recomendaciones de mejora.',
            'precio': 99.99,
            'activo': False,
            'orden': 5
        }
    ]
    
    productos_creados = 0
    
    for datos in productos_prueba:
        try:
            producto = ProductoSupabase(**datos)
            if producto.save():
                productos_creados += 1
                print(f"✅ Creado: {producto.titulo} (ID: {producto.id})")
            else:
                print(f"❌ Error creando: {datos['titulo']}")
        except Exception as e:
            print(f"❌ Error con {datos['titulo']}: {e}")
    
    print(f"\n🎉 {productos_creados} productos creados exitosamente")
    
    # Verificar productos
    print("\n📋 Productos en Supabase:")
    productos = ProductoSupabase.all()
    for p in productos:
        estado = "🟢 Activo" if p.activo else "🔴 Inactivo"
        print(f"  - {p.titulo} | ${p.precio} | {estado}")

if __name__ == "__main__":
    crear_productos_prueba()