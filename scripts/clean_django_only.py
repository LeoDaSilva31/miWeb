import os
import sys
import django

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
django.setup()

from catalogo.models import Producto  # Django ORM

def clean_django_products():
    """Elimina solo los productos de Django ORM"""
    
    print("🧹 Limpiando productos de Django ORM...")
    
    try:
        productos_django = Producto.objects.all()
        count = productos_django.count()
        
        if count > 0:
            print(f"🔄 Eliminando {count} productos de Django...")
            for producto in productos_django:
                print(f"🗑️ Eliminando: {producto.titulo}")
                # Eliminar archivo de imagen si existe
                if producto.foto:
                    try:
                        producto.foto.delete()
                    except:
                        pass
                producto.delete()
            print(f"✅ Eliminados {count} productos de Django ORM")
        else:
            print("✅ No hay productos en Django ORM")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("🎉 Limpieza de Django completada")

if __name__ == "__main__":
    clean_django_products()