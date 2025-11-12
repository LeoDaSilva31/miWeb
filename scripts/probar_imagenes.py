"""
Script para probar la subida y procesamiento de imágenes
"""
import sys
import os
sys.path.append('D:/miWeb')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
import django
django.setup()

from catalogo.supabase_models import ProductoSupabase
from miwebsite.supabase_config import upload_processed_image
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile

def crear_imagen_prueba(width=800, height=600, color=(66, 126, 234), text="Producto"):
    """
    Crea una imagen de prueba
    """
    image = Image.new('RGB', (width, height), color)
    
    # Agregar texto (si PIL tiene fuente disponible)
    try:
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(image)
        
        # Intentar usar una fuente por defecto
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Calcular posición del texto
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
    except:
        pass  # Si no se puede agregar texto, continuar
    
    # Guardar en buffer
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=95)
    buffer.seek(0)
    
    return buffer.getvalue()

def probar_subida_imagenes():
    """
    Prueba la subida y procesamiento de imágenes
    """
    print("🖼️ Probando subida y procesamiento de imágenes...")
    
    # Obtener algunos productos para agregarles imágenes
    productos = ProductoSupabase.activos()[:3]  # Tomar los primeros 3
    
    if not productos:
        print("❌ No hay productos para probar")
        return
    
    colores = [
        (66, 126, 234),   # Azul
        (52, 199, 89),    # Verde
        (255, 59, 48),    # Rojo
    ]
    
    for i, producto in enumerate(productos):
        try:
            print(f"\n📸 Creando imagen para: {producto.titulo}")
            
            # Crear imagen de prueba
            image_data = crear_imagen_prueba(
                width=1200, 
                height=800, 
                color=colores[i % len(colores)],
                text=producto.titulo[:20]
            )
            
            # Crear archivo Django fake
            fake_file = SimpleUploadedFile(
                name=f"imagen_{i+1}.jpg",
                content=image_data,
                content_type="image/jpeg"
            )
            
            print(f"📏 Tamaño original: {len(image_data)/1024:.1f} KB")
            
            # Subir y procesar imagen
            if producto.upload_image(fake_file):
                # Actualizar producto con nueva URL
                if producto.save():
                    print(f"✅ Imagen procesada y subida exitosamente")
                    print(f"🔗 URL: {producto.foto_url}")
                else:
                    print("❌ Error actualizando producto")
            else:
                print("❌ Error subiendo imagen")
                
        except Exception as e:
            print(f"❌ Error con {producto.titulo}: {e}")
    
    print(f"\n🎉 Proceso completado. Verifica el resultado en el navegador.")

if __name__ == "__main__":
    probar_subida_imagenes()