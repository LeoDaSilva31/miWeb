from django.contrib import admin
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
