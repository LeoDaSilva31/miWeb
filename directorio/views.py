from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Socio

def index(request):
    # Obtener algunos socios para mostrar inicialmente
    socios_destacados = Socio.objects.filter(activo=True)[:6]
    
    context = {
        'total_socios': Socio.objects.filter(activo=True).count(),
        'socios_destacados': socios_destacados,
        'es_demo': True,  # Para mostrar alertas de demo
    }
    return render(request, 'directorio/index.html', context)

def buscar(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        # Buscar en nombre, apellido, empresa
        socios = Socio.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(empresa__icontains=query),
            activo=True
        )
    else:
        socios = Socio.objects.filter(activo=True)[:10]
    
    # Si es petición AJAX, devolver JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        socios_data = []
        for socio in socios:
            socios_data.append({
                'id': socio.id,
                'nombre': socio.nombre,
                'apellido': socio.apellido,
                'email': socio.email,
                'telefono': socio.telefono,
                'empresa': socio.empresa,
                'fecha_registro': socio.fecha_registro.strftime('%d/%m/%Y'),
                'nombre_completo': socio.nombre_completo,
            })
        
        return JsonResponse({
            'socios': socios_data,
            'total': len(socios_data),
            'query': query
        })
    
    # Si no es AJAX, renderizar página completa
    context = {
        'socios': socios,
        'query': query,
        'total_resultados': socios.count(),
        'es_demo': True,
    }
    return render(request, 'directorio/resultados.html', context)
