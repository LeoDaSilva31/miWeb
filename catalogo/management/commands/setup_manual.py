"""
Comando de Django para configuración manual
"""
from django.core.management.base import BaseCommand
from scripts.setup_manual import create_productos_table_direct, create_bucket

class Command(BaseCommand):
    help = 'Configuración manual de Supabase'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Iniciando configuración manual de Supabase...'))
        
        # Crear bucket
        create_bucket()
        
        # Verificar tabla
        create_productos_table_direct()