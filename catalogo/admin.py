from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.shortcuts import render
from django.contrib import messages
from .models import Producto
from .supabase_models import ProductoSupabase

# Modelo proxy para gestionar productos de Supabase en el admin
class ProductoSupabaseProxy(Producto):
    class Meta:
        proxy = True
        verbose_name = 'Producto Supabase'
        verbose_name_plural = 'Productos Supabase'

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

@admin.register(ProductoSupabaseProxy)
class ProductoSupabaseAdmin(admin.ModelAdmin):
    """Admin personalizado que redirige a la interfaz de Supabase"""
    
    def has_module_permission(self, request):
        return True
    
    def has_view_permission(self, request, obj=None):
        return True
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def changelist_view(self, request, extra_context=None):
        """Redirigir a la vista de lista de Supabase"""
        return HttpResponseRedirect(reverse('catalogo:productos_supabase_list'))
    
    def add_view(self, request, form_url='', extra_context=None):
        """Redirigir a la vista de creación de Supabase"""
        return HttpResponseRedirect(reverse('catalogo:producto_supabase_create'))
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Redirigir a la vista de edición de Supabase"""
        return HttpResponseRedirect(reverse('catalogo:producto_supabase_update', args=[object_id]))
    
    def delete_view(self, request, object_id, extra_context=None):
        """Redirigir a la vista de eliminación de Supabase"""
        return HttpResponseRedirect(reverse('catalogo:producto_supabase_delete', args=[object_id]))
