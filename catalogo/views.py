from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Producto

def lista_productos(request):
    # Obtener productos activos ordenados
    productos_list = Producto.objects.filter(activo=True).order_by('orden', '-fecha_creacion')
    
    # Configurar paginador
    paginator = Paginator(productos_list, 20)  # 20 productos por página
    page_number = request.GET.get('page', 1)
    productos = paginator.get_page(page_number)
    
    context = {
        'productos': productos,
        'total_productos': productos_list.count(),
    }
    
    return render(request, 'catalogo/lista_productos.html', context)
