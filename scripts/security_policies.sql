-- ==========================================
-- POLÍTICAS DE SEGURIDAD PARA BUCKET mediaWeb
-- ==========================================

-- 1. ELIMINAR todas las políticas existentes del bucket mediaWeb
DELETE FROM storage.policies WHERE bucket_id = 'mediaWeb';

-- 2. CREAR políticas más seguras

-- Política 1: Lectura pública (cualquiera puede VER las imágenes)
INSERT INTO storage.policies (
    id, 
    bucket_id, 
    name, 
    definition, 
    operation
) VALUES (
    gen_random_uuid(),
    'mediaWeb', 
    'Lectura pública de imágenes', 
    'true', 
    'SELECT'
);

-- Política 2: Solo usuarios autenticados pueden SUBIR archivos
INSERT INTO storage.policies (
    id,
    bucket_id, 
    name, 
    check_definition, 
    operation
) VALUES (
    gen_random_uuid(),
    'mediaWeb', 
    'Solo autenticados pueden subir', 
    'auth.role() = ''authenticated''', 
    'INSERT'
);

-- Política 3: Solo usuarios autenticados pueden ACTUALIZAR archivos
INSERT INTO storage.policies (
    id,
    bucket_id, 
    name, 
    definition, 
    check_definition, 
    operation
) VALUES (
    gen_random_uuid(),
    'mediaWeb', 
    'Solo autenticados pueden actualizar', 
    'auth.role() = ''authenticated''', 
    'auth.role() = ''authenticated''', 
    'UPDATE'
);

-- Política 4: Solo usuarios autenticados pueden ELIMINAR archivos
INSERT INTO storage.policies (
    id,
    bucket_id, 
    name, 
    definition, 
    operation
) VALUES (
    gen_random_uuid(),
    'mediaWeb', 
    'Solo autenticados pueden eliminar', 
    'auth.role() = ''authenticated''', 
    'DELETE'
);

-- ==========================================
-- VERIFICAR que las políticas se crearon correctamente
-- ==========================================
SELECT 
    name, 
    operation, 
    definition, 
    check_definition
FROM storage.policies 
WHERE bucket_id = 'mediaWeb'
ORDER BY operation;