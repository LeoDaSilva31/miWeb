from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render
from django.contrib import messages
from django.core.files.storage import default_storage
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'activo', 'orden', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    list_editable = ('activo', 'orden')
    readonly_fields = ('fecha_creacion',)
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'descripcion', 'precio', 'foto')
        }),
        ('Configuración', {
            'fields': ('activo', 'orden')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
    
    def delete_model(self, request, obj):
        """
        Override delete_model to ensure S3/MinIO files are cleaned up
        even when deleting via Admin (which bypasses post_delete signals).
        """
        foto_name = getattr(obj.foto, 'name', None)
        if foto_name:
            try:
                if default_storage.exists(foto_name):
                    default_storage.delete(foto_name)
            except Exception:
                # log if needed, but don't block deletion
                pass
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        """
        Override delete_queryset to ensure S3/MinIO files are cleaned up
        when using bulk delete action (which also bypasses signals).
        """
        for obj in queryset:
            foto_name = getattr(obj.foto, 'name', None)
            if foto_name:
                try:
                    if default_storage.exists(foto_name):
                        default_storage.delete(foto_name)
                except Exception:
                    pass
        super().delete_queryset(request, queryset)

# Nota: Se eliminó la integración con Supabase. El admin gestiona ahora solo
# los modelos de Django definidos en `catalogo.models`.
