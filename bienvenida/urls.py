from django.urls import path
from . import views

app_name = 'bienvenida'

urlpatterns = [
    path('', views.index, name='index'),
]