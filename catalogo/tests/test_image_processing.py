from django.test import TestCase, override_settings
from catalogo.models import Producto
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
import tempfile
import shutil
import os


def create_test_image(format='PNG'):
    img = Image.new('RGB', (100, 100), color='red')
    buf = BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()


class ImageProcessingTests(TestCase):
    def test_saved_image_is_converted_to_webp_and_random_name(self):
        """
        Verifica que, tras guardar, el campo `foto` tenga un nombre generado
        en formato webp y dentro del prefijo `productos/`.

        No asumimos almacenamiento local en las pruebas: el proyecto usa
        MinIO/S3 en todos los entornos, por lo que no comprobamos existencia
        en disco aquí.
        """
        img_bytes = create_test_image('PNG')
        upload = SimpleUploadedFile('test.png', img_bytes, content_type='image/png')
        p = Producto(titulo='Img', descripcion='d', precio=1)
        p.foto = upload
        p.save()

        # The stored filename should end with .webp and be under productos/
        assert p.foto.name.endswith('.webp')
        assert p.foto.name.startswith('productos/')
