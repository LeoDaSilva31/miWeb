from django.shortcuts import render

def index(request):
    """
    Vista para mostrar la página de bienvenida con el mensaje 
    'Sitio en construcción'
    """
    return render(request, 'bienvenida/index.html')
