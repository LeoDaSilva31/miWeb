"""
Comando de Django para probar la conexión con Supabase
"""
from django.core.management.base import BaseCommand
from scripts.test_supabase import test_supabase_connection, show_current_config

class Command(BaseCommand):
    help = 'Prueba la conexión con Supabase'

    def handle(self, *args, **options):
        show_current_config()
        self.stdout.write("")
        
        if test_supabase_connection():
            self.stdout.write(self.style.SUCCESS('✅ Conexión con Supabase exitosa'))
        else:
            self.stdout.write(self.style.ERROR('❌ Error en la conexión con Supabase'))
            self.stdout.write(self.style.WARNING('💡 Revisa tu configuración en .env'))