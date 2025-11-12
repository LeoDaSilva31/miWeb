from django.urls import path
from . import views
from . import views_supabase

app_name = 'catalogo'

urlpatterns = [
    # URLs originales (Django ORM)
    path('productos/', views.lista_productos, name='lista_productos'),
    
    # URLs para Supabase
    path('admin/productos-supabase/', views_supabase.ProductosSupabaseListView.as_view(), name='productos_supabase_list'),
    path('admin/productos-supabase/crear/', views_supabase.ProductoSupabaseCreateView.as_view(), name='producto_supabase_create'),
    path('admin/productos-supabase/<str:producto_id>/editar/', views_supabase.ProductoSupabaseUpdateView.as_view(), name='producto_supabase_update'),
    path('admin/productos-supabase/<str:producto_id>/eliminar/', views_supabase.ProductoSupabaseDeleteView.as_view(), name='producto_supabase_delete'),
]