Carpeta de archivos no funcionales / temporales (basuras)

Se trasladaron aquí los archivos de prueba y otros elementos que no forman
parte del código fuente principal del proyecto.

Archivos movidos a `basuras/test/`:
- bienvenida/tests.py
- catalogo/tests.py

NOTA IMPORTANTE:
- No se movieron automáticamente la carpeta `.venv` ni el archivo `db.sqlite3`.
  Estos pueden contener datos importantes o estar en uso por el entorno.
  Si querés que los mueva aquí, confirmalo primero. Mover `.venv` puede romper
  tu entorno virtual activo; mover `db.sqlite3` trasladará la base de datos local.

Cómo mover manualmente (opcional):
  # en bash (Windows Git Bash)
  mv .venv basuras/.venv
  mv db.sqlite3 basuras/db.sqlite3

Si querés que lo haga automáticamente, decímelo y lo realizo (haré copia de
seguridad si lo preferís).
