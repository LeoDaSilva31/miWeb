"""
Vistas para gestionar productos de Supabase
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

from catalogo.supabase_models import ProductoSupabase
from catalogo.forms import ProductoSupabaseForm
from miwebsite.supabase_config import supabase_config

class ProductosSupabaseListView(View):
    """Vista para listar productos de Supabase"""
    
    def get(self, request):
        """Mostrar lista de productos"""
        if not supabase_config.is_configured():
            messages.error(request, "Supabase no está configurado")
            return redirect('admin:index')
        
        try:
            # Obtener todos los productos
            productos = ProductoSupabase.all()
            
            # Paginación
            paginator = Paginator(productos, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {
                'productos': page_obj,
                'title': 'Gestión de Productos - Supabase'
            }
            
            return render(request, 'admin/catalogo/productos_supabase_list.html', context)
            
        except Exception as e:
            messages.error(request, f"Error cargando productos: {e}")
            return render(request, 'admin/catalogo/productos_supabase_list.html', {'productos': []})

class ProductoSupabaseCreateView(View):
    """Vista para crear productos en Supabase"""
    
    def get(self, request):
        """Mostrar formulario de creación"""
        if not supabase_config.is_configured():
            messages.error(request, "Supabase no está configurado")
            return redirect('admin:index')
        
        form = ProductoSupabaseForm()
        context = {
            'form': form,
            'title': 'Crear Producto - Supabase',
            'action': 'crear'
        }
        return render(request, 'admin/catalogo/producto_supabase_form.html', context)
    
    def post(self, request):
        """Procesar creación de producto"""
        form = ProductoSupabaseForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Crear producto
                producto = ProductoSupabase(
                    titulo=form.cleaned_data['titulo'],
                    descripcion=form.cleaned_data['descripcion'],
                    precio=form.cleaned_data['precio'],
                    activo=form.cleaned_data['activo'],
                    orden=form.cleaned_data['orden']
                )
                
                # Guardar producto primero
                if producto.save():
                    # Procesar imagen si existe
                    foto = form.cleaned_data.get('foto')
                    if foto:
                        if producto.upload_image(foto):
                            # Actualizar con la URL de la imagen
                            producto.save()
                        else:
                            messages.warning(request, "Producto creado pero hubo un error subiendo la imagen")
                    
                    messages.success(request, f"Producto '{producto.titulo}' creado exitosamente")
                    return redirect('catalogo:productos_supabase_list')
                else:
                    messages.error(request, "Error guardando el producto")
                    
            except Exception as e:
                messages.error(request, f"Error creando producto: {e}")
        else:
            messages.error(request, f"Error en el formulario: {form.errors}")
        
        context = {
            'form': form,
            'title': 'Crear Producto - Supabase',
            'action': 'crear'
        }
        return render(request, 'admin/catalogo/producto_supabase_form.html', context)

class ProductoSupabaseUpdateView(View):
    """Vista para editar productos en Supabase"""
    
    def get(self, request, producto_id):
        """Mostrar formulario de edición"""
        if not supabase_config.is_configured():
            messages.error(request, "Supabase no está configurado")
            return redirect('admin:index')
        
        try:
            producto = ProductoSupabase.get_by_id(producto_id)
            if not producto:
                messages.error(request, "Producto no encontrado")
                return redirect('catalogo:productos_supabase_list')
            
            # Llenar formulario con datos del producto
            form = ProductoSupabaseForm(initial={
                'titulo': producto.titulo,
                'descripcion': producto.descripcion,
                'precio': producto.precio,
                'activo': producto.activo,
                'orden': producto.orden
            })
            
            context = {
                'form': form,
                'producto': producto,
                'title': f'Editar Producto - {producto.titulo}',
                'action': 'editar'
            }
            return render(request, 'admin/catalogo/producto_supabase_form.html', context)
            
        except Exception as e:
            messages.error(request, f"Error cargando producto: {e}")
            return redirect('catalogo:productos_supabase_list')
    
    def post(self, request, producto_id):
        """Procesar edición de producto"""
        try:
            producto = ProductoSupabase.get_by_id(producto_id)
            if not producto:
                messages.error(request, "Producto no encontrado")
                return redirect('catalogo:productos_supabase_list')
            
            form = ProductoSupabaseForm(request.POST, request.FILES)
            
            if form.is_valid():
                # Actualizar campos
                producto.titulo = form.cleaned_data['titulo']
                producto.descripcion = form.cleaned_data['descripcion']
                producto.precio = form.cleaned_data['precio']
                producto.activo = form.cleaned_data['activo']
                producto.orden = form.cleaned_data['orden']
                
                # Procesar nueva imagen si existe
                foto = form.cleaned_data.get('foto')
                if foto:
                    if not producto.upload_image(foto):
                        messages.warning(request, "Error subiendo la nueva imagen")
                
                # Guardar cambios
                if producto.save():
                    messages.success(request, f"Producto '{producto.titulo}' actualizado exitosamente")
                    return redirect('catalogo:productos_supabase_list')
                else:
                    messages.error(request, "Error guardando los cambios")
            
            context = {
                'form': form,
                'producto': producto,
                'title': f'Editar Producto - {producto.titulo}',
                'action': 'editar'
            }
            return render(request, 'admin/catalogo/producto_supabase_form.html', context)
            
        except Exception as e:
            messages.error(request, f"Error editando producto: {e}")
            return redirect('catalogo:productos_supabase_list')

class ProductoSupabaseDeleteView(View):
    """Vista para eliminar productos en Supabase"""
    
    def post(self, request, producto_id):
        """Eliminar producto"""
        if not supabase_config.is_configured():
            return JsonResponse({'success': False, 'error': 'Supabase no configurado'})
        
        try:
            producto = ProductoSupabase.get_by_id(producto_id)
            if not producto:
                return JsonResponse({'success': False, 'error': 'Producto no encontrado'})
            
            titulo = producto.titulo
            
            # Eliminar imagen del bucket
            producto.delete_image()
            
            # Eliminar producto
            if producto.delete():
                return JsonResponse({
                    'success': True, 
                    'message': f"Producto '{titulo}' eliminado exitosamente"
                })
            else:
                return JsonResponse({
                    'success': False, 
                    'error': 'Error eliminando el producto'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': f'Error: {str(e)}'
            })