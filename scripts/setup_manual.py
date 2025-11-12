"""
Script alternativo para crear la tabla productos directamente
"""
from miwebsite.supabase_config import get_supabase_client

def create_productos_table_direct():
    """
    Crea la tabla productos usando la API de Supabase
    """
    client = get_supabase_client()
    
    if not client:
        print("❌ Error: No se pudo conectar a Supabase")
        return False
    
    print("🚀 Creando tabla productos en Supabase...")
    
    try:
        # Intentar crear algunos registros de prueba para verificar que funciona
        # Primero verificamos si la tabla existe intentando hacer una consulta
        try:
            response = client.table('productos').select('id').limit(1).execute()
            print("✅ La tabla 'productos' ya existe")
            return True
        except Exception as e:
            if "does not exist" in str(e).lower() or "relation" in str(e).lower():
                print("📋 La tabla 'productos' no existe, necesita ser creada manualmente")
                print("\n🔧 Ejecuta el siguiente SQL en el SQL Editor de Supabase:")
                print_sql_commands()
                return False
            else:
                print(f"❌ Error verificando tabla: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def print_sql_commands():
    """
    Imprime los comandos SQL que deben ejecutarse manualmente
    """
    sql = """
-- 1. Crear tabla productos
CREATE TABLE IF NOT EXISTS productos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2),
    foto_url TEXT,
    activo BOOLEAN DEFAULT true,
    orden INTEGER DEFAULT 0,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Crear índices
CREATE INDEX IF NOT EXISTS idx_productos_activo ON productos(activo);
CREATE INDEX IF NOT EXISTS idx_productos_orden ON productos(orden);
CREATE INDEX IF NOT EXISTS idx_productos_fecha_creacion ON productos(fecha_creacion);

-- 3. Crear función para actualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 4. Crear trigger
CREATE TRIGGER IF NOT EXISTS update_productos_updated_at
    BEFORE UPDATE ON productos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 5. Habilitar RLS
ALTER TABLE productos ENABLE ROW LEVEL SECURITY;

-- 6. Crear políticas
CREATE POLICY IF NOT EXISTS "Productos activos son públicamente legibles"
    ON productos FOR SELECT
    USING (activo = true);

CREATE POLICY IF NOT EXISTS "Usuarios autenticados pueden gestionar productos"
    ON productos FOR ALL
    USING (auth.role() = 'authenticated');
"""
    
    print(sql)
    print("\n📝 Instrucciones:")
    print("1. Ve a tu proyecto en https://app.supabase.com")
    print("2. Ve a SQL Editor")
    print("3. Copia y pega el SQL de arriba")
    print("4. Haz clic en 'Run' para ejecutarlo")
    print("5. Vuelve a ejecutar: python manage.py test_table")

def create_bucket():
    """
    Crea el bucket de productos-images
    """
    client = get_supabase_client()
    
    if not client:
        return False
    
    try:
        # Crear bucket
        storage = client.storage
        result = storage.create_bucket('productos-images', public=True)
        print("✅ Bucket 'productos-images' creado exitosamente")
        return True
    except Exception as e:
        if "already exists" in str(e):
            print("ℹ️ Bucket 'productos-images' ya existe")
            return True
        else:
            print(f"❌ Error creando bucket: {e}")
            return False

if __name__ == "__main__":
    print("🔧 Verificando y configurando Supabase...")
    
    # Crear bucket
    create_bucket()
    
    # Verificar/crear tabla
    create_productos_table_direct()