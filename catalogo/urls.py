from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    # URLs originales (Django ORM)
    path('productos/', views.lista_productos, name='lista_productos'),
]