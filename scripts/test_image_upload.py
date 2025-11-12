import os
import sys
import django

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from miwebsite.supabase_config import upload_processed_image
import requests

def test_image_upload():
    """Prueba la subida y procesamiento de imágenes"""
    
    # Descargar imagen de prueba
    print("🔄 Descargando imagen de prueba...")
    try:
        response = requests.get("https://picsum.photos/1200/800", timeout=10)
        if response.status_code == 200:
            image_data = response.content
            print("✅ Imagen descargada exitosamente")
        else:
            print(f"❌ Error descargando imagen: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error descargando imagen: {e}")
        return
    
    # Crear archivo simulado
    uploaded_file = SimpleUploadedFile(
        "test_image.jpg",
        image_data,
        content_type="image/jpeg"
    )
    
    print(f"📸 Tamaño original: {len(image_data) / (1024*1024):.2f} MB")
    
    # Procesar y subir imagen
    print("🔄 Procesando y subiendo imagen...")
    try:
        imagen_url = upload_processed_image(uploaded_file, "test")
        
        if imagen_url:
            print(f"✅ ¡Imagen subida exitosamente!")
            print(f"🔗 URL: {imagen_url}")
            
            # Probar acceso a la imagen
            print("🔄 Verificando acceso público...")
            test_response = requests.get(imagen_url, timeout=10)
            if test_response.status_code == 200:
                print("✅ ¡La imagen es accesible públicamente!")
                print(f"📏 Tamaño final: {len(test_response.content) / (1024*1024):.2f} MB")
            else:
                print(f"❌ Error accediendo a la imagen: {test_response.status_code}")
                
        else:
            print("❌ Error: La subida falló")
            
    except Exception as e:
        print(f"❌ Error durante la subida: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Iniciando prueba de subida de imágenes a Supabase...")
    test_image_upload()
    print("🏁 Prueba completada")