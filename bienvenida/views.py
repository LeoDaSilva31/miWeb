from django.shortcuts import render
from django.core.paginator import Paginator
from catalogo.supabase_models import ProductoSupabase
from miwebsite.supabase_config import supabase_config

def index(request):
    """
    Vista para mostrar la página de bienvenida con productos de Supabase
    """
    productos = None
    
    # Usar exclusivamente Supabase
    if supabase_config.is_configured():
        productos_list = ProductoSupabase.ordenados()
        
        if productos_list:
            paginator = Paginator(productos_list, 20)
            page_number = request.GET.get('page', 1)
            productos = paginator.get_page(page_number)
    
    context = {
        'productos': productos,
        'usando_supabase': True,
    }
    
    return render(request, 'bienvenida/index.html', context)
