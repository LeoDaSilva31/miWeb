"""
Modelos para trabajar con Supabase
Este archivo contiene clases que representan tablas en Supabase
"""
from django.conf import settings
from miwebsite.supabase_config import get_supabase_client
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class SupabaseModel:
    """
    Clase base para modelos que usan Supabase como backend
    """
    table_name: str = ""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def get_client(cls):
        """Obtiene el cliente Supabase"""
        return get_supabase_client()
    
    @classmethod
    def all(cls) -> List['SupabaseModel']:
        """Obtiene todos los registros de la tabla"""
        client = cls.get_client()
        if not client:
            return []
        
        try:
            response = client.table(cls.table_name).select("*").execute()
            return [cls(**item) for item in response.data]
        except Exception as e:
            print(f"Error obteniendo registros: {e}")
            return []
    
    @classmethod
    def filter(cls, **filters) -> List['SupabaseModel']:
        """Filtra registros por campos específicos"""
        client = cls.get_client()
        if not client:
            return []
        
        try:
            query = client.table(cls.table_name).select("*")
            
            for field, value in filters.items():
                query = query.eq(field, value)
            
            response = query.execute()
            return [cls(**item) for item in response.data]
        except Exception as e:
            print(f"Error filtrando registros: {e}")
            return []
    
    @classmethod
    def get_by_id(cls, record_id: str) -> Optional['SupabaseModel']:
        """Obtiene un registro por ID"""
        client = cls.get_client()
        if not client:
            return None
        
        try:
            response = client.table(cls.table_name).select("*").eq("id", record_id).execute()
            if response.data:
                return cls(**response.data[0])
            return None
        except Exception as e:
            print(f"Error obteniendo registro por ID: {e}")
            return None
    
    def save(self) -> bool:
        """Guarda el registro en Supabase"""
        client = self.get_client()
        if not client:
            return False
        
        try:
            data = self.to_dict()
            
            if hasattr(self, 'id') and self.id:
                # Actualizar registro existente
                response = client.table(self.table_name).update(data).eq("id", self.id).execute()
            else:
                # Crear nuevo registro - remover ID None para que PostgreSQL genere uno
                if 'id' in data and data['id'] is None:
                    del data['id']
                
                response = client.table(self.table_name).insert(data).execute()
                
                # Obtener el ID generado
                if response.data and len(response.data) > 0:
                    self.id = response.data[0]['id']
            
            return bool(response.data)
        except Exception as e:
            print(f"Error guardando registro: {e}")
            return False
    
    def delete(self) -> bool:
        """Elimina el registro de Supabase"""
        if not hasattr(self, 'id'):
            return False
            
        client = self.get_client()
        if not client:
            return False
        
        try:
            response = client.table(self.table_name).delete().eq("id", self.id).execute()
            return bool(response.data)
        except Exception as e:
            print(f"Error eliminando registro: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario"""
        from decimal import Decimal
        
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                # Convertir Decimal a float para JSON serialization
                if isinstance(value, Decimal):
                    data[key] = float(value)
                else:
                    data[key] = value
        return data


class ProductoSupabase(SupabaseModel):
    """
    Modelo para productos usando Supabase
    """
    table_name = "productos"
    
    def __init__(self, **kwargs):
        # Campos del producto
        self.id: Optional[str] = kwargs.get('id')
        self.titulo: str = kwargs.get('titulo', '')
        self.descripcion: str = kwargs.get('descripcion', '')
        self.precio: Optional[float] = kwargs.get('precio')
        self.foto_url: Optional[str] = kwargs.get('foto_url')
        self.activo: bool = kwargs.get('activo', True)
        self.orden: int = kwargs.get('orden', 0)
        self.fecha_creacion: Optional[str] = kwargs.get('fecha_creacion')
        self.fecha_actualizacion: Optional[str] = kwargs.get('fecha_actualizacion')
        
        super().__init__(**kwargs)
    
    @property
    def foto(self):
        """Compatibilidad con template Django - simula el campo foto"""
        if self.foto_url:
            return type('FakeImageField', (), {'url': self.foto_url})()
        return None
    
    @classmethod
    def activos(cls) -> List['ProductoSupabase']:
        """Obtiene solo los productos activos"""
        return cls.filter(activo=True)
    
    @classmethod
    def ordenados(cls) -> List['ProductoSupabase']:
        """Obtiene productos ordenados"""
        client = cls.get_client()
        if not client:
            return []
        
        try:
            response = client.table(cls.table_name).select("*").eq("activo", True).order("orden", desc=False).order("fecha_creacion", desc=True).execute()
            return [cls(**item) for item in response.data]
        except Exception as e:
            print(f"Error obteniendo productos ordenados: {e}")
            return []
    
    def save(self) -> bool:
        """Guarda el producto con timestamps automáticos"""
        now = datetime.now().isoformat()
        
        if not hasattr(self, 'id') or not self.id:
            self.fecha_creacion = now
        
        self.fecha_actualizacion = now
        
        return super().save()
    
    def upload_image(self, image_file) -> bool:
        """
        Procesa y sube una imagen para este producto
        
        Args:
            image_file: Archivo de imagen (Django UploadedFile)
            
        Returns:
            bool: True si se subió exitosamente
        """
        from miwebsite.supabase_config import upload_processed_image
        
        # Eliminar imagen anterior si existe
        if self.foto_url:
            self.delete_image()
        
        # Subir nueva imagen procesada
        new_url = upload_processed_image(image_file, f"productos/{self.id or 'temp'}")
        
        if new_url:
            self.foto_url = new_url
            return True
        
        return False
    
    def delete_image(self) -> bool:
        """
        Elimina la imagen asociada del bucket
        
        Returns:
            bool: True si se eliminó exitosamente
        """
        from miwebsite.supabase_config import delete_image_from_bucket
        
        if not self.foto_url:
            return True
        
        try:
            # Extraer la ruta del archivo de la URL
            if '/productos/' in self.foto_url:
                file_path = self.foto_url.split('/productos/', 1)[1]
                file_path = f"productos/{file_path}"
                return delete_image_from_bucket(file_path)
        except Exception as e:
            print(f"Error eliminando imagen: {e}")
        
        return False
    
    def __str__(self):
        return self.titulo
    
    def __repr__(self):
        return f"ProductoSupabase(id='{self.id}', titulo='{self.titulo}')"