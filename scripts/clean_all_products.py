import os
import sys
import django

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
django.setup()

from catalogo.supabase_models import ProductoSupabase
from catalogo.models import Producto  # Django ORM
from miwebsite.supabase_config import supabase_config

def clean_all_products():
    """Elimina TODOS los productos tanto de Supabase como Django ORM"""
    
    print("🧹 LIMPIEZA COMPLETA - Eliminando todos los productos...")
    
    # 1. Eliminar TODOS los productos de Supabase
    print("🔄 Eliminando todos los productos de Supabase...")
    try:
        productos_supabase = ProductoSupabase.all()
        
        for producto in productos_supabase:
            print(f"🗑️ Eliminando de Supabase: {producto.titulo}")
            # Eliminar imagen primero si existe
            if producto.foto_url:
                producto.delete_image()
            # Eliminar producto
            producto.delete()
            
        print(f"✅ Eliminados {len(productos_supabase)} productos de Supabase")
            
    except Exception as e:
        print(f"❌ Error eliminando productos de Supabase: {e}")
    
    # 2. Eliminar TODOS los productos de Django ORM
    print("🔄 Eliminando todos los productos de Django ORM...")
    try:
        productos_django = Producto.objects.all()
        count = productos_django.count()
        
        for producto in productos_django:
            print(f"🗑️ Eliminando de Django: {producto.nombre}")
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
    
    # 3. Limpiar todas las carpetas del bucket
    print("🔄 Limpiando TODAS las carpetas del bucket...")
    try:
        if supabase_config.is_configured():
            storage = supabase_config.service_client.storage
            
            # Limpiar carpeta productos
            try:
                productos_files = storage.from_(supabase_config.bucket_name).list("productos")
                if productos_files:
                    file_paths = [f"productos/{file['name']}" for file in productos_files if file.get('name')]
                    if file_paths:
                        storage.from_(supabase_config.bucket_name).remove(file_paths)
                        print(f"✅ Eliminados {len(file_paths)} archivos de carpeta productos")
            except Exception as e:
                print(f"⚠️ Error limpiando carpeta productos: {e}")
            
            # Limpiar carpeta test
            try:
                test_files = storage.from_(supabase_config.bucket_name).list("test")
                if test_files:
                    file_paths = [f"test/{file['name']}" for file in test_files if file.get('name')]
                    if file_paths:
                        storage.from_(supabase_config.bucket_name).remove(file_paths)
                        print(f"✅ Eliminados {len(file_paths)} archivos de carpeta test")
            except Exception as e:
                print(f"⚠️ Error limpiando carpeta test: {e}")
                
    except Exception as e:
        print(f"❌ Error limpiando bucket: {e}")
    
    print("🎉 LIMPIEZA COMPLETA TERMINADA")
    print("🚀 Ahora puedes crear productos desde cero en el admin!")

if __name__ == "__main__":
    clean_all_products()