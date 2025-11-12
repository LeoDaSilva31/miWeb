from django.db import models
from django.utils import timezone

class Producto(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    foto = models.ImageField(upload_to='productos/', verbose_name="Foto")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
    orden = models.IntegerField(default=0, verbose_name="Orden", help_text="Número para ordenar los productos")
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['orden', '-fecha_creacion']
    
    def __str__(self):
        return self.titulo
