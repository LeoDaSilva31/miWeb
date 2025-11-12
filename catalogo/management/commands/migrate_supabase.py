"""
Comando de Django para migrar a Supabase
"""
from django.core.management.base import BaseCommand
from scripts.migrate_supabase import run_migrations

class Command(BaseCommand):
    help = 'Ejecuta las migraciones para configurar Supabase'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando migraciones de Supabase...'))
        
        success = run_migrations()
        
        if success:
            self.stdout.write(self.style.SUCCESS('🎉 ¡Migraciones completadas exitosamente!'))
        else:
            self.stdout.write(self.style.ERROR('❌ Error durante las migraciones'))
            self.stdout.write(self.style.WARNING('💡 Verifica tu configuración en .env'))