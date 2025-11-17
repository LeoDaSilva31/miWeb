#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def _ensure_venv_sitepackages():
    """If psycopg/psycopg2 isn't importable, try to add .venv site-packages to sys.path.

    This helps when users run `python manage.py` with the system Python instead of
    activating the project's virtualenv. It only attempts to add `.venv` located
    at the project root and prefers Windows layout first, then Unix layout.
    """
    try:
        import psycopg  # type: ignore
        return
    except Exception:
        pass
    try:
        import psycopg2  # type: ignore
        return
    except Exception:
        pass

    project_root = Path(__file__).resolve().parent
    venv_root = project_root / '.venv'
    if not venv_root.exists():
        return

    # Windows layout: .venv/Lib/site-packages
    candidates = [venv_root / 'Lib' / 'site-packages']
    # Unix layout: .venv/lib/pythonX.Y/site-packages
    py_dirs = sorted(venv_root.glob('lib/python*'))
    for d in py_dirs:
        candidates.append(d / 'site-packages')

    for p in candidates:
        if p.exists():
            # Insert at front so packages in venv take precedence
            sys.path.insert(0, str(p))
            print(f"Added .venv site-packages to sys.path: {p}")
            # One attempt is enough — importing psycopg should now succeed if installed
            return



def main():
    """Run administrative tasks."""
    # try to ensure .venv site-packages are on sys.path so commands work even if
    # the developer forgot to activate the virtualenv
    _ensure_venv_sitepackages()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miwebsite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
