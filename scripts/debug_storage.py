import os
import sys
import django

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
django.setup()

from miwebsite.supabase_config import supabase_config

def debug_supabase_storage():
    """Debug del estado del storage"""
    
    if not supabase_config.is_configured():
        print("❌ Supabase no está configurado")
        return
        
    try:
        # Listar archivos en el bucket
        print("🔄 Listando archivos en el bucket...")
        storage = supabase_config.client.storage
        files = storage.from_(supabase_config.bucket_name).list()
        print(f"📂 Archivos encontrados: {files}")
        
        # Listar archivos en carpeta test
        print("🔄 Listando archivos en carpeta test...")
        test_files = storage.from_(supabase_config.bucket_name).list("test")
        print(f"📂 Archivos en test: {test_files}")
        
        if test_files:
            # Intentar obtener URL pública del primer archivo
            first_file = test_files[0]
            file_path = f"test/{first_file['name']}"
            print(f"🔄 Obteniendo URL pública de: {file_path}")
            
            public_url = storage.from_(supabase_config.bucket_name).get_public_url(file_path)
            print(f"🔗 URL pública: {public_url}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Debug del storage de Supabase...")
    debug_supabase_storage()