from django.test import TestCase, Client
from django.urls import reverse
from catalogo.models import Producto
from django.db import DatabaseError
from unittest.mock import patch


class ApiProductosTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_productos_returns_products(self):
        Producto.objects.create(titulo='P1', descripcion='d', precio=10)
        Producto.objects.create(titulo='P2', descripcion='d2', precio=20, activo=False)
        # only activo=True should be returned
        resp = self.client.get('/api/productos/')
        assert resp.status_code == 200
        data = resp.json()
        assert 'productos' in data
        assert len(data['productos']) == 1

    def test_api_productos_db_error_returns_empty_list(self):
        # Patch the correct model manager (Producto) to simulate DB errors
        with patch('catalogo.models.Producto.objects.filter') as mock_filter:
            mock_filter.side_effect = DatabaseError('DB down')
            resp = self.client.get('/api/productos/')
            assert resp.status_code == 200
            data = resp.json()
            assert data.get('productos') == []
