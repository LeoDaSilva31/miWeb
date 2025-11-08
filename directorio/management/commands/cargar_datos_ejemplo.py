from django.core.management.base import BaseCommand
from directorio.models import Socio
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Carga datos de ejemplo para el directorio'

    def handle(self, *args, **options):
        # Borrar datos existentes
        Socio.objects.all().delete()
        
        # Datos de ejemplo
        socios_data = [
            {
                'nombre': 'Juan Carlos',
                'apellido': 'García López',
                'email': 'juan.garcia@tecnologia.com',
                'telefono': '+54 11 4567-8901',
                'empresa': 'TecnologíaPro S.A.',
            },
            {
                'nombre': 'María Elena',
                'apellido': 'Rodríguez Silva',
                'email': 'maria.rodriguez@consultora.com',
                'telefono': '+54 11 4567-8902',
                'empresa': 'Consultora Estratégica',
            },
            {
                'nombre': 'Carlos Alberto',
                'apellido': 'Méndez Torres',
                'email': 'carlos.mendez@innovacion.com',
                'telefono': '+54 11 4567-8903',
                'empresa': 'Innovación Digital',
            },
            {
                'nombre': 'Ana Patricia',
                'apellido': 'Fernández Vega',
                'email': 'ana.fernandez@marketing.com',
                'telefono': '+54 11 4567-8904',
                'empresa': 'Marketing Integral',
            },
            {
                'nombre': 'Roberto Miguel',
                'apellido': 'Sánchez Ruiz',
                'email': 'roberto.sanchez@construccion.com',
                'telefono': '+54 11 4567-8905',
                'empresa': 'Construcciones del Sur',
            },
            {
                'nombre': 'Laura Beatriz',
                'apellido': 'Morales Castro',
                'email': 'laura.morales@salud.com',
                'telefono': '+54 11 4567-8906',
                'empresa': 'Centro de Salud Integral',
            },
            {
                'nombre': 'Diego Alejandro',
                'apellido': 'Romero Paz',
                'email': 'diego.romero@educacion.com',
                'telefono': '+54 11 4567-8907',
                'empresa': 'Instituto Educativo Moderno',
            },
            {
                'nombre': 'Carmen Rosa',
                'apellido': 'Herrera Díaz',
                'email': 'carmen.herrera@comercio.com',
                'telefono': '+54 11 4567-8908',
                'empresa': 'Comercio Internacional',
            },
            {
                'nombre': 'Fernando Luis',
                'apellido': 'Jiménez Vargas',
                'email': 'fernando.jimenez@logistica.com',
                'telefono': '+54 11 4567-8909',
                'empresa': 'Logística y Transporte',
            },
            {
                'nombre': 'Gabriela Sofia',
                'apellido': 'Cruz Ramírez',
                'email': 'gabriela.cruz@financiera.com',
                'telefono': '+54 11 4567-8910',
                'empresa': 'Financiera Nacional',
            },
            {
                'nombre': 'Andrés Felipe',
                'apellido': 'López Martín',
                'email': 'andres.lopez@energia.com',
                'telefono': '+54 11 4567-8911',
                'empresa': 'Energía Renovable',
            },
            {
                'nombre': 'Valeria Alejandra',
                'apellido': 'Guerrero Núñez',
                'email': 'valeria.guerrero@diseno.com',
                'telefono': '+54 11 4567-8912',
                'empresa': 'Diseño y Arquitectura',
            },
        ]

        # Crear socios
        socios_creados = 0
        for data in socios_data:
            socio = Socio.objects.create(
                nombre=data['nombre'],
                apellido=data['apellido'],
                email=data['email'],
                telefono=data['telefono'],
                empresa=data['empresa'],
                activo=True
            )
            socios_creados += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'✅ Se crearon {socios_creados} socios de ejemplo exitosamente')
        )
        self.stdout.write(
            self.style.SUCCESS(f'🔍 El sistema está listo para probar la búsqueda')
        )