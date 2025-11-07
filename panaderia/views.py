from django.shortcuts import render

def index(request):
    """Vista principal de la panadería"""
    context = {
        'panaderia_nombre': 'Panadería del Hogar',
        'telefono_whatsapp': '5491123456789',  # Formato internacional
        'mensaje_whatsapp': '¡Hola! Me interesa conocer más sobre sus productos frescos',
        'instagram': 'panaderiahogar',
        'facebook': 'panaderiahogar',
    }
    return render(request, 'panaderia/index.html', context)
