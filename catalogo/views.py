from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import timedelta
import json

from .models import Producto, ProductoLike, ProductoComentario
from .forms import ProductoComentarioForm


def get_client_id(request):
    """
    Obtiene un ID único para el cliente (usuario anónimo o autenticado).
    Para usuarios autenticados: usa el user_id
    Para anónimos: usa la IP (o sesión)
    """
    if request.user.is_authenticated:
        return f"user_{request.user.id}"
    else:
        # Obtener IP del cliente
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return f"ip_{ip}"


def lista_productos(request):
    """Vista principal de productos."""
    productos_list = Producto.objects.filter(activo=True).order_by('orden', '-fecha_creacion')
    
    paginator = Paginator(productos_list, 20)
    page_number = request.GET.get('page', 1)
    productos = paginator.get_page(page_number)
    
    context = {
        'productos': productos,
        'total_productos': productos_list.count(),
    }
    
    return render(request, 'catalogo/lista_productos.html', context)


# ============================================================
#  API Endpoints para likes/dislikes
# ============================================================

@require_http_methods(["POST"])
def api_producto_like(request, producto_id):
    """
    Endpoint para dar/cambiar like o dislike a un producto.
    
    POST: {
        "tipo": "like" | "dislike"
    }
    """
    try:
        producto = get_object_or_404(Producto, id=producto_id)
        cliente_id = get_client_id(request)
        
        data = json.loads(request.body)
        tipo = data.get('tipo')
        
        if tipo not in ['like', 'dislike']:
            return JsonResponse({'error': 'Tipo inválido. Debe ser "like" o "dislike".'}, status=400)
        
        # Obtener o crear el like/dislike
        like_obj, created = ProductoLike.objects.get_or_create(
            producto=producto,
            usuario_id=cliente_id,
            defaults={'tipo': tipo}
        )
        
        # Si ya existe, actualizar el tipo (cambiar de like a dislike o viceversa)
        if not created:
            if like_obj.tipo == tipo:
                # Si es el mismo tipo, eliminar el voto (toggle off)
                like_obj.delete()
                return JsonResponse({
                    'success': True,
                    'accion': 'removed',
                    'likes': producto.likes.filter(tipo='like').count(),
                    'dislikes': producto.likes.filter(tipo='dislike').count(),
                })
            else:
                # Cambiar de tipo
                like_obj.tipo = tipo
                like_obj.save()
        
        return JsonResponse({
            'success': True,
            'accion': 'created' if created else 'updated',
            'likes': producto.likes.filter(tipo='like').count(),
            'dislikes': producto.likes.filter(tipo='dislike').count(),
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def api_producto_stats(request, producto_id):
    """Obtiene estadísticas de likes/dislikes de un producto."""
    try:
        producto = get_object_or_404(Producto, id=producto_id)
        cliente_id = get_client_id(request)
        
        # Obtener voto del usuario actual
        voto_actual = None
        try:
            voto = ProductoLike.objects.get(producto=producto, usuario_id=cliente_id)
            voto_actual = voto.tipo
        except ProductoLike.DoesNotExist:
            pass
        
        return JsonResponse({
            'likes': producto.likes.filter(tipo='like').count(),
            'dislikes': producto.likes.filter(tipo='dislike').count(),
            'voto_actual': voto_actual,
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================
#  API Endpoints para comentarios
# ============================================================

@require_http_methods(["POST"])
def api_comentario_crear(request, producto_id):
    """
    Crea un nuevo comentario en un producto.
    
    POST: {
        "texto": "Mi comentario aquí..."
    }
    """
    try:
        producto = get_object_or_404(Producto, id=producto_id)
        cliente_id = get_client_id(request)
        
        # Verificar que pueda comentar hoy
        if not ProductoComentario.puede_comentar_hoy(producto_id, cliente_id):
            return JsonResponse({
                'error': 'Ya has comentado en este producto hoy. Intenta mañana.'
            }, status=429)  # 429 Too Many Requests
        
        data = json.loads(request.body)
        texto = data.get('texto', '').strip()
        
        if not texto:
            return JsonResponse({'error': 'El comentario no puede estar vacío.'}, status=400)
        
        if len(texto) > 200:
            return JsonResponse({'error': 'El comentario no puede exceder 200 caracteres.'}, status=400)
        
        # Crear el comentario
        comentario = ProductoComentario.objects.create(
            producto=producto,
            usuario_id=cliente_id,
            texto=texto
        )
        
        return JsonResponse({
            'success': True,
            'comentario': {
                'id': comentario.id,
                'texto': comentario.texto,
                'usuario_id': comentario.usuario_id,
                'fecha_creacion': comentario.fecha_creacion.isoformat(),
            }
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def api_comentarios_lista(request, producto_id):
    """Obtiene lista de comentarios de un producto."""
    try:
        producto = get_object_or_404(Producto, id=producto_id)
        
        # Paginación
        page = request.GET.get('page', 1)
        paginator = Paginator(
            producto.comentarios.all(),
            20  # 20 comentarios por página
        )
        comments_page = paginator.get_page(page)
        
        comentarios = [
            {
                'id': c.id,
                'texto': c.texto,
                'usuario_id': c.usuario_id,
                'fecha_creacion': c.fecha_creacion.isoformat(),
            }
            for c in comments_page
        ]
        
        return JsonResponse({
            'comentarios': comentarios,
            'total': paginator.count,
            'page': comments_page.number,
            'total_pages': paginator.num_pages,
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["DELETE"])
def api_comentario_eliminar(request, comentario_id):
    """
    Elimina un comentario (solo el propietario o admin).
    """
    try:
        comentario = get_object_or_404(ProductoComentario, id=comentario_id)
        cliente_id = get_client_id(request)
        
        # Verificar que sea el propietario o admin
        if comentario.usuario_id != cliente_id and not request.user.is_staff:
            return JsonResponse({'error': 'No tienes permiso para eliminar este comentario.'}, status=403)
        
        comentario.delete()
        
        return JsonResponse({'success': True, 'mensaje': 'Comentario eliminado'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
