"""
URL configuration for miwebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
import os

def robots_txt(request):
    robots_path = os.path.join(settings.BASE_DIR, 'robots.txt')
    with open(robots_path, 'r') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/plain')

def sitemap_xml(request):
    sitemap_path = os.path.join(settings.BASE_DIR, 'sitemap.xml')
    with open(sitemap_path, 'r') as f:
        content = f.read()
    return HttpResponse(content, content_type='application/xml')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bienvenida.urls')),
    path('catalogo/', include('catalogo.urls')),
    
    # SEO URLs
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
