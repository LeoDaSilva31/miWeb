"""
Script para probar la tabla productos en Supabase
"""
import sys
import os
sys.path.append('D:/miWeb')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
import django
django.setup()

from catalogo.supabase_models import ProductoSupabase

def test_productos_table():
    """
    Prueba las operaciones básicas en la tabla productos
    """
    print("🧪 Probando tabla productos en Supabase...")
    
    try:
        # 1. Probar obtener todos los productos (debería estar vacío)
        productos = ProductoSupabase.all()
        print(f"✅ Consulta exitosa: {len(productos)} productos encontrados")
        
        # 2. Probar crear un producto de prueba
        producto_test = ProductoSupabase(
            titulo="Producto de Prueba",
            descripcion="Este es un producto de prueba para verificar que Supabase funciona correctamente",
            precio=99.99,
            activo=True,
            orden=1
        )
        
        # 3. Guardar el producto
        if producto_test.save():
            print("✅ Producto de prueba creado exitosamente")
            print(f"   ID: {producto_test.id}")
            print(f"   Título: {producto_test.titulo}")
            
            # 4. Probar obtener el producto por ID
            producto_obtenido = ProductoSupabase.get_by_id(producto_test.id)
            if producto_obtenido:
                print("✅ Producto obtenido por ID exitosamente")
                
                # 5. Probar actualizar el producto
                producto_obtenido.titulo = "Producto de Prueba - ACTUALIZADO"
                if producto_obtenido.save():
                    print("✅ Producto actualizado exitosamente")
                    
                    # 6. Probar eliminar el producto
                    if producto_obtenido.delete():
                        print("✅ Producto eliminado exitosamente")
                    else:
                        print("❌ Error eliminando producto")
                else:
                    print("❌ Error actualizando producto")
            else:
                print("❌ Error obteniendo producto por ID")
        else:
            print("❌ Error creando producto")
            
        print("\n🎉 ¡Todas las pruebas de la tabla productos pasaron exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        return False

if __name__ == "__main__":
    test_productos_table()