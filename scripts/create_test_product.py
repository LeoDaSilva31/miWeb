import os
import sys
import django

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
django.setup()

from catalogo.supabase_models import ProductoSupabase
from django.core.files.uploadedfile import SimpleUploadedFile
import requests

def create_test_product():
    """Crea un producto de prueba con imagen desde Supabase"""
    
    print("🔄 Descargando imagen de prueba...")
    try:
        response = requests.get("https://picsum.photos/800/600", timeout=10)
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
        "producto_test.jpg",
        image_data,
        content_type="image/jpeg"
    )
    
    print(f"📸 Tamaño original: {len(image_data) / (1024*1024):.2f} MB")
    
    try:
        # Crear producto con imagen
        print("🔄 Creando producto en Supabase...")
        
        # Crear instancia del producto
        producto = ProductoSupabase(
            titulo="Producto de Prueba Supabase",
            descripcion="Este es un producto creado automáticamente para probar la integración con Supabase y el procesamiento de imágenes.",
            precio=99.99,
            activo=True,
            orden=1
        )
        
        # Guardar producto primero
        if producto.save():
            print(f"✅ Producto guardado en base de datos")
            print(f"🏷️ Nombre: {producto.titulo}")
            print(f"💰 Precio: ${producto.precio}")
            
            # Ahora subir la imagen
            print("� Subiendo imagen procesada...")
            if producto.upload_image(uploaded_file):
                print("✅ ¡Imagen subida y procesada exitosamente!")
                
                # Guardar con la URL actualizada
                producto.save()
                
                foto_url = producto.foto_url
                if foto_url:
                    print(f"🔗 URL de imagen: {foto_url}")
                    
                    # Verificar acceso a la imagen
                    print("🔄 Verificando acceso a la imagen...")
                    test_response = requests.get(foto_url, timeout=10)
                    if test_response.status_code == 200:
                        print("✅ ¡La imagen es accesible públicamente!")
                        print(f"📏 Tamaño final: {len(test_response.content) / (1024*1024):.2f} MB")
                    else:
                        print(f"❌ Error accediendo a la imagen: {test_response.status_code}")
                else:
                    print("⚠️ No se generó URL de imagen")
            else:
                print("❌ Error subiendo imagen")
        else:
            print("❌ Error: No se pudo guardar el producto")
            
    except Exception as e:
        print(f"❌ Error creando producto: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Creando producto de prueba con imagen...")
    create_test_product()
    print("🏁 Prueba completada")