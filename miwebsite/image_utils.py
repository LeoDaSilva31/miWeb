"""
Utilidades para procesamiento de imágenes
"""
from PIL import Image
import io
import os
from typing import Tuple, Optional
from django.core.files.uploadedfile import UploadedFile

def process_image_for_web(image_file: UploadedFile, max_size_mb: int = 2) -> Tuple[bytes, str]:
    """
    Procesa una imagen para web: reescala, convierte a WebP y limita el tamaño
    
    Args:
        image_file: Archivo de imagen subido
        max_size_mb: Tamaño máximo en MB (default: 2MB)
    
    Returns:
        Tuple[bytes, str]: (datos_imagen_procesada, nuevo_nombre_archivo)
    """
    # Abrir imagen con Pillow
    image = Image.open(image_file)
    
    # Convertir a RGB si es necesario (para WebP)
    if image.mode in ('RGBA', 'LA'):
        # Para imágenes con transparencia, usar fondo blanco
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'RGBA':
            background.paste(image, mask=image.split()[-1])  # usar canal alpha como máscara
        else:
            background.paste(image)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Obtener dimensiones originales
    original_width, original_height = image.size
    
    # Calcular nuevas dimensiones manteniendo proporción
    # Máximo 1920px de ancho para pantallas Full HD
    max_width = 1920
    max_height = 1080
    
    if original_width > max_width or original_height > max_height:
        # Calcular ratio para mantener proporción
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        
        # Reescalar imagen
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Generar nuevo nombre de archivo con extensión .jpg (más compatible)
    original_name = os.path.splitext(image_file.name)[0]
    new_filename = f"{original_name}.jpg"
    
    # Convertir a JPEG con diferentes calidades hasta conseguir tamaño objetivo
    max_size_bytes = max_size_mb * 1024 * 1024
    quality = 85
    
    while quality >= 30:  # Mínima calidad aceptable
        buffer = io.BytesIO()
        image.save(buffer, format='JPEG', quality=quality, optimize=True)
        image_bytes = buffer.getvalue()
        
        if len(image_bytes) <= max_size_bytes:
            break
            
        quality -= 10
    
    # Si aún es muy grande, reducir dimensiones
    if len(image_bytes) > max_size_bytes:
        scale_factor = 0.8
        while len(image_bytes) > max_size_bytes and scale_factor > 0.3:
            current_width, current_height = image.size
            new_width = int(current_width * scale_factor)
            new_height = int(current_height * scale_factor)
            
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            resized_image.save(buffer, format='JPEG', quality=75, optimize=True)
            image_bytes = buffer.getvalue()
            
            image = resized_image
            scale_factor -= 0.1
    
    return image_bytes, new_filename


def validate_image_file(image_file: UploadedFile) -> bool:
    """
    Valida que el archivo sea una imagen válida
    
    Args:
        image_file: Archivo subido
        
    Returns:
        bool: True si es válida, False si no
    """
    try:
        # Verificar que sea una imagen
        image = Image.open(image_file)
        image.verify()  # Verificar integridad
        
        # Resetear el puntero del archivo
        image_file.seek(0)
        
        # Verificar extensiones permitidas
        allowed_formats = ['JPEG', 'JPG', 'PNG', 'GIF', 'BMP', 'WEBP']
        if image.format in allowed_formats:
            return True
        
        return False
    except Exception:
        return False


def get_image_info(image_file: UploadedFile) -> dict:
    """
    Obtiene información de la imagen
    
    Args:
        image_file: Archivo de imagen
        
    Returns:
        dict: Información de la imagen
    """
    try:
        image = Image.open(image_file)
        info = {
            'format': image.format,
            'mode': image.mode,
            'size': image.size,
            'width': image.size[0],
            'height': image.size[1],
            'file_size': len(image_file.read())
        }
        image_file.seek(0)  # Resetear puntero
        return info
    except Exception:
        return {}