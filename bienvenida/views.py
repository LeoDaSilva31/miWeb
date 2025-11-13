from django.shortcuts import render
from django.core.paginator import Paginator
from catalogo.models import Producto


def index(request):
    """
    Vista para mostrar la página de bienvenida usando los modelos de Django
    """
    productos = None

    try:
        productos_list = Producto.objects.filter(activo=True).order_by('orden', '-fecha_creacion')

        if productos_list:
            paginator = Paginator(productos_list, 20)
            page_number = request.GET.get('page', 1)
            productos = paginator.get_page(page_number)

    except Exception:
        productos = []

    context = {
        'productos': productos,
        'usando_supabase': False,
    }

    return render(request, 'bienvenida/index.html', context)
