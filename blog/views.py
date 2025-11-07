from django.shortcuts import render

def index(request):
    """
    Vista principal del blog de Leo
    """
    return render(request, 'blog/index.html')
