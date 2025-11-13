"""
Script alternativo que imprime los comandos SQL necesarios para crear la
tabla `productos` en PostgreSQL (útil para pgAdmin o psql).
"""

def print_sql_commands():
    """
    Imprime los comandos SQL que deben ejecutarse manualmente en PostgreSQL
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

    print("\n📝 Instrucciones para pgAdmin / psql:")
    print("1. Abre pgAdmin o conéctate con psql a tu servidor PostgreSQL local")
    print("2. Crea el usuario/DB si no existen (ej.: CREATE USER miweb WITH PASSWORD 'miweb'; CREATE DATABASE miweb OWNER miweb;")
    print("3. Ejecuta el SQL de arriba en la base de datos objetivo")
    print("4. Verifica con: \"\d productos\" en psql o inspeccionando la tabla en pgAdmin")

if __name__ == "__main__":
    print("🔧 Imprimiendo SQL para crear tabla 'productos' en PostgreSQL")
    print_sql_commands()