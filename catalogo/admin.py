from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render
from django.contrib import messages
from django.core.files.storage import default_storage
from .models import Producto, ProductoLike, ProductoComentario

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


@admin.register(ProductoLike)
class ProductoLikeAdmin(admin.ModelAdmin):
    list_display = ('usuario_id', 'producto', 'tipo', 'fecha_creacion')
    list_filter = ('tipo', 'fecha_creacion')
    search_fields = ('usuario_id', 'producto__titulo')
    readonly_fields = ('fecha_creacion',)
    
    fieldsets = (
        ('Información', {
            'fields': ('producto', 'usuario_id', 'tipo')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductoComentario)
class ProductoComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario_id', 'producto', 'texto_preview', 'fecha_creacion')
    list_filter = ('fecha_creacion', 'producto')
    search_fields = ('usuario_id', 'producto__titulo', 'texto')
    readonly_fields = ('fecha_creacion', 'texto')
    
    fieldsets = (
        ('Información', {
            'fields': ('producto', 'usuario_id', 'texto')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
    
    def texto_preview(self, obj):
        """Mostrar vista previa del comentario."""
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_preview.short_description = 'Comentario'
    
    def has_add_permission(self, request):
        """No permitir agregar comentarios desde admin (solo vía API)."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Los comentarios son inmutables."""
        return False

# Nota: Se eliminó la integración con Supabase. El admin gestiona ahora solo
# los modelos de Django definidos en `catalogo.models`.
