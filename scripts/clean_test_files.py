import os
import sys
import django

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
django.setup()

from catalogo.supabase_models import ProductoSupabase
from miwebsite.supabase_config import supabase_config

def clean_test_files():
    """Limpia archivos de prueba del bucket y base de datos"""
    
    print("🧹 Iniciando limpieza de archivos de prueba...")
    
    # 1. Eliminar productos de prueba de la base de datos
    print("🔄 Eliminando productos de prueba de Supabase...")
    try:
        productos_prueba = ProductoSupabase.filter(titulo__icontains="Prueba")
        
        for producto in productos_prueba:
            print(f"🗑️ Eliminando producto: {producto.titulo}")
            # Eliminar imagen primero
            if producto.foto_url:
                producto.delete_image()
            # Eliminar producto
            producto.delete()
            
        print(f"✅ Eliminados {len(productos_prueba)} productos de prueba")
            
    except Exception as e:
        print(f"❌ Error eliminando productos: {e}")
    
    # 2. Limpiar carpeta test del bucket
    print("🔄 Limpiando carpeta 'test' del bucket...")
    try:
        if supabase_config.is_configured():
            storage = supabase_config.service_client.storage
            
            # Listar archivos en carpeta test
            test_files = storage.from_(supabase_config.bucket_name).list("test")
            
            if test_files:
                # Eliminar todos los archivos de la carpeta test
                file_paths = [f"test/{file['name']}" for file in test_files]
                storage.from_(supabase_config.bucket_name).remove(file_paths)
                print(f"✅ Eliminados {len(file_paths)} archivos de prueba del bucket")
            else:
                print("📂 No hay archivos en la carpeta test")
                
    except Exception as e:
        print(f"❌ Error limpiando bucket: {e}")
    
    print("🎉 Limpieza completada")

if __name__ == "__main__":
    clean_test_files()