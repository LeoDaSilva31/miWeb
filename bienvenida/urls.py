from django.urls import path
from . import views

app_name = 'bienvenida'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/productos/', views.api_productos, name='api_productos'),
    path('debug/product-photos/', views.debug_product_photos, name='debug_product_photos'),
]