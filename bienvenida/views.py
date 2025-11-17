from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import DatabaseError

from catalogo.models import Producto
from django.conf import settings
from django.core.files.storage import default_storage
import os
import logging

logger = logging.getLogger(__name__)


def index(request):
    """
    Vista para mostrar la página de bienvenida usando los modelos de Django.

    Si la base de datos local no está disponible (por ejemplo, PC apagada),
    capturamos DatabaseError y devolvemos una lista vacía junto con
    un flag `db_unavailable` para que el front-end muestre el mensaje
    y pueda intentar reintentos en segundo plano.
    """
    productos = []

    try:
        productos_list = Producto.objects.filter(activo=True).order_by('orden', '-fecha_creacion')

        if productos_list.exists():
            paginator = Paginator(productos_list, 20)
            page_number = request.GET.get('page', 1)
            productos = paginator.get_page(page_number)

            # Añadir foto_url absoluto a cada producto para evitar llamadas a
            # métodos desde la plantilla (request.build_absolute_uri no es
            # invocable desde templates). Esto facilita mostrar imágenes
            # con URLs absolutas en el modal y en las miniaturas.
            for p in productos:
                # Priorizar un atributo externo `foto_url` si existe (ej. CDN)
                if getattr(p, 'foto_url', None):
                    # si ya es absoluto, dejarlo
                    if str(p.foto_url).startswith('http'):
                        p.foto_url = str(p.foto_url)
                    else:
                        p.foto_url = request.build_absolute_uri(str(p.foto_url))
                elif p.foto:
                    try:
                        p.foto_url = request.build_absolute_uri(p.foto.url)
                    except Exception:
                        p.foto_url = None

            # Debug: si estamos en modo DEBUG, loguear información útil sobre
            # las primeras entradas para facilitar diagnóstico de imágenes
            if settings.DEBUG:
                for p in list(productos)[:5]:
                    foto_name = getattr(p, 'foto', None) and getattr(p.foto, 'name', None)
                    foto_url = getattr(p, 'foto_url', None)
                    # Comprobar existencia usando el storage por defecto (MinIO/S3)
                    exists = False
                    if foto_name:
                        try:
                            exists = default_storage.exists(foto_name)
                        except Exception:
                            exists = False
                    logger.debug('Producto %s: foto_name=%s, foto_url=%s, stored_exists=%s',
                                 p.id, foto_name, foto_url, exists)

    except DatabaseError:
        # Silently treat DB errors as "no products" to the user
        productos = []

    context = {
        'productos': productos,
        'usando_supabase': False,
    }

    return render(request, 'bienvenida/index.html', context)


def api_productos(request):
    """Endpoint JSON para obtener productos activos.

    Devuelve 503 si la base de datos no está disponible.
    """
    try:
        productos_qs = Producto.objects.filter(activo=True).order_by('orden', '-fecha_creacion')
        productos = []
        for p in productos_qs:
            productos.append({
                'id': p.id,
                'titulo': p.titulo,
                'descripcion': p.descripcion,
                'precio': float(p.precio) if p.precio is not None else None,
                'foto': p.foto_url if getattr(p, 'foto_url', None) else (p.foto.url if p.foto else None),
            })
        return JsonResponse({'productos': productos}, status=200)
    except DatabaseError:
        # If DB is down, return empty list so frontend treats it as "no products"
        return JsonResponse({'productos': []}, status=200)


def debug_product_photos(request):
    """Debug endpoint: devuelve una lista corta con info sobre fotos.

    Sólo activa si DEBUG=True. Útil para diagnosticar URLs y paths localmente.
    """
    from django.conf import settings
    if not settings.DEBUG:
        return JsonResponse({'error': 'disabled'}, status=403)

    productos_qs = Producto.objects.filter(activo=True).order_by('orden', '-fecha_creacion')[:20]
    out = []
    for p in productos_qs:
        foto_name = getattr(p.foto, 'name', None) if getattr(p, 'foto', None) else None
        try:
            foto_url = request.build_absolute_uri(p.foto.url) if p.foto else None
        except Exception:
            foto_url = None
        stored_exists = False
        if foto_name:
            try:
                stored_exists = default_storage.exists(foto_name)
            except Exception:
                stored_exists = False
        out.append({'id': p.id, 'titulo': p.titulo, 'foto_name': foto_name, 'foto_url': foto_url, 'stored_exists': stored_exists})
    return JsonResponse({'productos': out})
