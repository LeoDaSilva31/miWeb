"""
Configuración y utilidades para Supabase
"""
import os
from django.conf import settings
from typing import Optional

# Importación condicional de supabase (se instalará después)
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

class SupabaseConfig:
    """
    Clase para manejar la configuración y conexión con Supabase
    """
    
    def __init__(self):
        self.url: str = settings.SUPABASE_URL
        self.key: str = settings.SUPABASE_KEY
        self.service_key: str = settings.SUPABASE_SERVICE_KEY
        self.bucket_name: str = settings.SUPABASE_BUCKET_NAME
        self._client: Optional[Client] = None
        self._service_client: Optional[Client] = None
    
    @property
    def client(self) -> Optional[Client]:
        """
        Cliente Supabase para operaciones generales
        """
        if not SUPABASE_AVAILABLE:
            return None
            
        if self._client is None and self.url and self.key:
            self._client = create_client(self.url, self.key)
        return self._client
    
    @property
    def service_client(self) -> Optional[Client]:
        """
        Cliente Supabase con service key para operaciones administrativas
        """
        if not SUPABASE_AVAILABLE:
            return None
            
        if self._service_client is None and self.url and self.service_key:
            self._service_client = create_client(self.url, self.service_key)
        return self._service_client
    
    def is_configured(self) -> bool:
        """
        Verifica si Supabase está configurado correctamente
        """
        return all([
            SUPABASE_AVAILABLE,
            self.url,
            self.key,
            self.url != 'tu_supabase_url_aqui',
            self.key != 'tu_supabase_anon_key_aqui'
        ])
    
    def get_storage_client(self):
        """
        Cliente para manejar storage/buckets
        """
        if self.client:
            return self.client.storage
        return None

# Instancia global
supabase_config = SupabaseConfig()


def get_supabase_client() -> Optional[Client]:
    """
    Función helper para obtener el cliente Supabase
    """
    return supabase_config.client


def upload_image_to_bucket(file_data: bytes, file_name: str, folder: str = "productos") -> Optional[str]:
    """
    Sube una imagen al bucket de Supabase
    
    Args:
        file_data: Datos del archivo en bytes
        file_name: Nombre del archivo
        folder: Carpeta dentro del bucket
        
    Returns:
        URL pública de la imagen o None si falla
    """
    if not supabase_config.is_configured():
        return None
    
    try:
        storage = supabase_config.get_storage_client()
        if not storage:
            return None
            
        # Crear el bucket si no existe
        try:
            storage.create_bucket(supabase_config.bucket_name, public=True)
        except:
            pass  # El bucket ya existe
        
        # Subir archivo
        file_path = f"{folder}/{file_name}"
        
        # Verificar si el archivo ya existe y eliminarlo
        try:
            storage.from_(supabase_config.bucket_name).remove([file_path])
        except:
            pass  # El archivo no existe, continuar
        
        result = storage.from_(supabase_config.bucket_name).upload(file_path, file_data, file_options={"content-type": "image/jpeg"})
        
        if result:
            # Obtener URL pública
            url_result = storage.from_(supabase_config.bucket_name).get_public_url(file_path)
            return url_result
            
    except Exception as e:
        print(f"Error subiendo imagen a Supabase: {e}")
        
    return None


def upload_processed_image(image_file, folder: str = "productos") -> Optional[str]:
    """
    Procesa y sube una imagen al bucket de Supabase usando service key
    
    Args:
        image_file: Archivo de imagen (Django UploadedFile)
        folder: Carpeta dentro del bucket
        
    Returns:
        URL pública de la imagen procesada o None si falla
    """
    from miwebsite.image_utils import process_image_for_web, validate_image_file
    import uuid
    
    if not validate_image_file(image_file):
        print("Error: El archivo no es una imagen válida")
        return None
    
    try:
        # Procesar imagen
        processed_image_data, processed_filename = process_image_for_web(image_file)
        
        # Generar nombre único
        unique_name = f"{uuid.uuid4()}_{processed_filename}"
        
        # Subir imagen procesada usando service client (más permisos)
        return upload_image_to_bucket_with_service_key(processed_image_data, unique_name, folder)
        
    except Exception as e:
        print(f"Error procesando y subiendo imagen: {e}")
        return None


def upload_image_to_bucket_with_service_key(file_data: bytes, file_name: str, folder: str = "productos") -> Optional[str]:
    """
    Sube una imagen al bucket usando service key para permisos administrativos
    """
    if not supabase_config.is_configured():
        return None
    
    try:
        # Usar service client para operaciones administrativas
        service_client = supabase_config.service_client
        if not service_client:
            return None
        
        storage = service_client.storage
        
        # Subir archivo
        file_path = f"{folder}/{file_name}"
        
        # Verificar si el archivo ya existe y eliminarlo
        try:
            storage.from_(supabase_config.bucket_name).remove([file_path])
        except:
            pass  # El archivo no existe, continuar
        
        result = storage.from_(supabase_config.bucket_name).upload(file_path, file_data, file_options={"content-type": "image/jpeg"})
        
        if result:
            # Obtener URL pública
            url_result = storage.from_(supabase_config.bucket_name).get_public_url(file_path)
            return url_result
            
    except Exception as e:
        print(f"Error subiendo imagen a Supabase: {e}")
        
    return None


def delete_image_from_bucket(file_path: str) -> bool:
    """
    Elimina una imagen del bucket de Supabase
    
    Args:
        file_path: Ruta del archivo en el bucket
        
    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    if not supabase_config.is_configured():
        return False
    
    try:
        storage = supabase_config.get_storage_client()
        if not storage:
            return False
            
        result = storage.from_(supabase_config.bucket_name).remove([file_path])
        return bool(result)
        
    except Exception as e:
        print(f"Error eliminando imagen de Supabase: {e}")
        
    return False