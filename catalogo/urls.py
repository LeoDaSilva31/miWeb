from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    # Vista principal
    path('productos/', views.lista_productos, name='lista_productos'),
    
    # API: Likes/Dislikes
    path('api/productos/<int:producto_id>/like/', views.api_producto_like, name='api_like'),
    path('api/productos/<int:producto_id>/stats/', views.api_producto_stats, name='api_stats'),
    
    # API: Comentarios
    path('api/productos/<int:producto_id>/comentarios/', views.api_comentarios_lista, name='api_comentarios_lista'),
    path('api/productos/<int:producto_id>/comentarios/crear/', views.api_comentario_crear, name='api_comentario_crear'),
    path('api/comentarios/<int:comentario_id>/eliminar/', views.api_comentario_eliminar, name='api_comentario_eliminar'),
]