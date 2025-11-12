"""
Script de migración para crear las tablas necesarias en Supabase
"""
from miwebsite.supabase_config import get_supabase_client

def create_productos_table():
    """
    SQL para crear la tabla productos en Supabase
    """
    sql = """
    -- Crear tabla productos
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

    -- Crear índices para mejorar rendimiento
    CREATE INDEX IF NOT EXISTS idx_productos_activo ON productos(activo);
    CREATE INDEX IF NOT EXISTS idx_productos_orden ON productos(orden);
    CREATE INDEX IF NOT EXISTS idx_productos_fecha_creacion ON productos(fecha_creacion);

    -- Crear trigger para actualizar fecha_actualizacion automáticamente
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.fecha_actualizacion = NOW();
        RETURN NEW;
    END;
    $$ language 'plpgsql';

    CREATE TRIGGER IF NOT EXISTS update_productos_updated_at
        BEFORE UPDATE ON productos
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();

    -- Habilitar RLS (Row Level Security) si es necesario
    ALTER TABLE productos ENABLE ROW LEVEL SECURITY;

    -- Política para permitir lectura pública de productos activos
    CREATE POLICY IF NOT EXISTS "Productos activos son públicamente legibles"
        ON productos FOR SELECT
        USING (activo = true);

    -- Política para permitir todas las operaciones a usuarios autenticados
    CREATE POLICY IF NOT EXISTS "Usuarios autenticados pueden gestionar productos"
        ON productos FOR ALL
        USING (auth.role() = 'authenticated');
    """
    return sql

def create_bucket_and_policies():
    """
    SQL para crear bucket de imágenes y políticas
    """
    sql = """
    -- Crear bucket para imágenes de productos (esto se hace desde la interfaz o con storage client)
    -- INSERT INTO storage.buckets (id, name, public) VALUES ('productos-images', 'productos-images', true);

    -- Políticas para el bucket de imágenes
    CREATE POLICY IF NOT EXISTS "Imágenes de productos públicamente visibles"
        ON storage.objects FOR SELECT
        USING (bucket_id = 'productos-images');

    CREATE POLICY IF NOT EXISTS "Usuarios autenticados pueden subir imágenes"
        ON storage.objects FOR INSERT
        WITH CHECK (bucket_id = 'productos-images' AND auth.role() = 'authenticated');

    CREATE POLICY IF NOT EXISTS "Usuarios autenticados pueden actualizar imágenes"
        ON storage.objects FOR UPDATE
        USING (bucket_id = 'productos-images' AND auth.role() = 'authenticated');

    CREATE POLICY IF NOT EXISTS "Usuarios autenticados pueden eliminar imágenes"
        ON storage.objects FOR DELETE
        USING (bucket_id = 'productos-images' AND auth.role() = 'authenticated');
    """
    return sql

def run_migrations():
    """
    Ejecuta las migraciones en Supabase
    """
    client = get_supabase_client()
    
    if not client:
        print("❌ Error: No se pudo conectar a Supabase")
        print("Verifica que las credenciales en .env sean correctas")
        return False
    
    print("🚀 Iniciando migraciones en Supabase...")
    
    try:
        # Crear tabla productos
        print("📋 Creando tabla productos...")
        productos_sql = create_productos_table()
        client.rpc('exec_sql', {'sql': productos_sql}).execute()
        print("✅ Tabla productos creada exitosamente")
        
        # Crear bucket de imágenes
        print("🗂️ Configurando bucket de imágenes...")
        try:
            storage = client.storage
            storage.create_bucket('productos-images', public=True)
            print("✅ Bucket 'productos-images' creado exitosamente")
        except Exception as e:
            if "already exists" in str(e):
                print("ℹ️ Bucket 'productos-images' ya existe")
            else:
                print(f"⚠️ Advertencia creando bucket: {e}")
        
        # Aplicar políticas de storage
        print("🔒 Configurando políticas de seguridad...")
        storage_sql = create_bucket_and_policies()
        client.rpc('exec_sql', {'sql': storage_sql}).execute()
        print("✅ Políticas de seguridad configuradas")
        
        print("\n🎉 ¡Migraciones completadas exitosamente!")
        print("📊 Tu base de datos Supabase está lista para usar")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante las migraciones: {e}")
        return False

if __name__ == "__main__":
    run_migrations()