import os
import sys
import django

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
django.setup()

from catalogo.models import Producto  # Django ORM

def clean_all_products():
    """Elimina TODOS los productos del ORM de Django (útil para reiniciar catálogo)."""
    
    print("🧹 LIMPIEZA COMPLETA - Eliminando todos los productos...")
    
    # 1. Eliminar TODOS los productos de Django ORM
    print("🔄 Eliminando todos los productos de Django ORM...")
    try:
        productos_django = Producto.objects.all()
        count = productos_django.count()
        
        for producto in productos_django:
            print(f"🗑️ Eliminando de Django: {producto.titulo}")
            # Eliminar archivo de imagen si existe
            if producto.foto:
                try:
                    producto.foto.delete()
                except:
                    pass
            producto.delete()
            
        print(f"✅ Eliminados {count} productos de Django ORM")
            
    except Exception as e:
        print(f"❌ Error eliminando productos de Django: {e}")
    
    print("🎉 LIMPIEZA COMPLETA TERMINADA")
    print("🚀 Ahora puedes crear productos desde cero en el admin!")

if __name__ == "__main__":
    clean_all_products()