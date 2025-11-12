"""
Script para verificar la conexión con Supabase
"""
from miwebsite.supabase_config import supabase_config, get_supabase_client

def test_supabase_connection():
    """
    Verifica que la conexión con Supabase funcione correctamente
    """
    print("🔍 Verificando configuración de Supabase...")
    
    # Verificar configuración
    if not supabase_config.is_configured():
        print("❌ Error: Supabase no está configurado correctamente")
        print("📝 Verifica las siguientes variables en tu archivo .env:")
        print("   - SUPABASE_URL")
        print("   - SUPABASE_KEY")
        print("   - SUPABASE_SERVICE_KEY")
        print("   - SUPABASE_BUCKET_NAME")
        return False
    
    print("✅ Configuración básica correcta")
    
    # Probar conexión
    print("🔗 Probando conexión con Supabase...")
    client = get_supabase_client()
    
    if not client:
        print("❌ Error: No se pudo crear el cliente Supabase")
        return False
    
    try:
        # Probar una query simple (obtener información del usuario actual)
        response = client.auth.get_user()
        print("✅ Conexión establecida exitosamente")
        
        # Probar acceso a storage
        storage = client.storage
        buckets = storage.list_buckets()
        print(f"✅ Acceso a storage confirmado ({len(buckets)} buckets disponibles)")
        
        # Verificar si existe el bucket de productos
        bucket_name = supabase_config.bucket_name
        bucket_exists = any(bucket['name'] == bucket_name for bucket in buckets)
        
        if bucket_exists:
            print(f"✅ Bucket '{bucket_name}' encontrado")
        else:
            print(f"⚠️ Bucket '{bucket_name}' no encontrado (se creará durante las migraciones)")
        
        print("\n🎉 ¡Supabase está listo para usar!")
        return True
        
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que las credenciales sean correctas")
        print("   2. Asegúrate de que el proyecto Supabase esté activo")
        print("   3. Revisa que las claves tengan los permisos necesarios")
        return False

def show_current_config():
    """
    Muestra la configuración actual (sin mostrar las claves completas por seguridad)
    """
    print("\n📋 Configuración actual:")
    print(f"   URL: {supabase_config.url}")
    print(f"   Key: {supabase_config.key[:20]}..." if supabase_config.key else "   Key: No configurada")
    print(f"   Service Key: {supabase_config.service_key[:20]}..." if supabase_config.service_key else "   Service Key: No configurada")
    print(f"   Bucket: {supabase_config.bucket_name}")

if __name__ == "__main__":
    show_current_config()
    print()
    test_supabase_connection()