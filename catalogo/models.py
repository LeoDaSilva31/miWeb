import uuid
import re
from io import BytesIO
from PIL import Image

from django.db import models
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver


# ============================================================
#  Función para generar nombres de archivo basados en el título
# ============================================================

def clean_filename(text):
    """
    Convierte el título del producto en un nombre seguro:
    - minúsculas
    - espacios -> guiones
    - caracteres especiales -> eliminados
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9áéíóúñü ]', '', text)  # dejar solo letras/números/espacios
    text = text.replace(" ", "-")
    return text


def generate_image_name(instance, ext="webp"):
    """
    Crea un nombre único basado en el título del producto.
    Ejemplo: figura-gundam-azul_imagen.webp
    """
    base = clean_filename(instance.titulo)
    filename = f"{base}_imagen.{ext}"

    # Verificar si ya existe en el storage → agregar sufijo único
    storage_path = f"productos/{filename}"
    if default_storage.exists(storage_path):
        unique = uuid.uuid4().hex[:6]
        filename = f"{base}_{unique}_imagen.{ext}"

    return f"productos/{filename}"


# ============================================================
#                         Modelo
# ============================================================

class Producto(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    foto = models.ImageField(upload_to="productos/", verbose_name="Foto")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
    orden = models.IntegerField(default=0, verbose_name="Orden")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["orden", "-fecha_creacion"]

    def __str__(self):
        return self.titulo

    # ============================================================
    #  Procesamiento de imagen → conversión a WebP + 3MB máx
    # ============================================================
    def save(self, *args, **kwargs):
        try:
            foto_field = getattr(self, "foto", None)

            if foto_field and hasattr(foto_field, "file") and foto_field.file:

                # Leer imagen original
                foto_field.file.seek(0)
                img = Image.open(foto_field.file)

                # Convertir modos
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

                # Convertir a WebP
                output = BytesIO()
                img.save(output, format="WEBP", quality=80, method=6)
                output.seek(0)

                # Generar nombre basado en título
                storage_path = generate_image_name(self, ext="webp")

                # Guardar en MinIO
                default_storage.save(storage_path, ContentFile(output.read()))

                # Comprimir si pesa más de 3 MB
                max_bytes = 3 * 1024 * 1024

                def current_size():
                    try:
                        return default_storage.size(storage_path)
                    except Exception:
                        return None

                size = current_size()

                # Reducir calidad progresivamente
                if size and size > max_bytes:
                    for quality in (70, 60, 50, 40, 30):
                        temp = BytesIO()
                        img.save(temp, format="WEBP", quality=quality, method=6)
                        temp.seek(0)

                        default_storage.delete(storage_path)
                        default_storage.save(storage_path, ContentFile(temp.read()))

                        size = current_size()
                        if size and size <= max_bytes:
                            break

                # Redimensionar si aún supera el límite
                if size and size > max_bytes:
                    width, height = img.size
                    scale = 0.9
                    while size > max_bytes and min(width, height) > 200:
                        width = int(width * scale)
                        height = int(height * scale)
                        resized = img.resize((width, height), Image.LANCZOS)

                        temp = BytesIO()
                        resized.save(temp, format="WEBP", quality=30, method=6)
                        temp.seek(0)

                        default_storage.delete(storage_path)
                        default_storage.save(storage_path, ContentFile(temp.read()))

                        size = current_size()
                        scale -= 0.05

                # Reemplazar nombre final
                self.foto.name = storage_path

        except Exception:
            pass

        super().save(*args, **kwargs)


# ============================================================
#  Señales → borrar imagen al editar o eliminar producto
# ============================================================

@receiver(pre_save, sender=Producto)
def delete_old_file_on_change(sender, instance, **kwargs):
    """
    Cuando se reemplaza la foto de un Producto,
    borrar el archivo anterior del storage (MinIO).
    """
    if not instance.pk:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if old.foto and old.foto != instance.foto:
        storage = old.foto.storage
        name = old.foto.name
        if name:
            storage.delete(name)


@receiver(post_delete, sender=Producto)
def delete_file_on_delete(sender, instance, **kwargs):
    """
    Cuando se borra un Producto, borrar también el archivo
    de la foto en MinIO.
    """
    if instance.foto:
        storage = instance.foto.storage
        name = instance.foto.name
        if name:
            storage.delete(name)
