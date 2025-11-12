"""
Script para crear el bucket en Supabase
"""
import sys
import os
sys.path.append('D:/miWeb')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
import django
django.setup()

from miwebsite.supabase_config import get_supabase_client, supabase_config

def crear_bucket():
    """
    Crea el bucket productos-images en Supabase
    """
    client = get_supabase_client()
    
    if not client:
        print("❌ No se pudo conectar a Supabase")
        return False
    
    try:
        storage = client.storage
        
        # Listar buckets existentes
        print("📋 Buckets existentes:")
        buckets = storage.list_buckets()
        for bucket in buckets:
            print(f"  - {bucket['name']} (público: {bucket.get('public', False)})")
        
        bucket_name = supabase_config.bucket_name
        
        # Verificar si el bucket ya existe
        bucket_exists = any(bucket['name'] == bucket_name for bucket in buckets)
        
        if bucket_exists:
            print(f"✅ El bucket '{bucket_name}' ya existe")
            return True
        
        # Crear bucket público
        print(f"🗂️ Creando bucket '{bucket_name}'...")
        
        # Intentar crear bucket con la nueva API
        try:
            result = storage.create_bucket(bucket_name, {"public": True})
            print(f"✅ Bucket '{bucket_name}' creado exitosamente")
            return True
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"ℹ️ El bucket '{bucket_name}' ya existe")
                return True
            else:
                print(f"❌ Error creando bucket: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    crear_bucket()