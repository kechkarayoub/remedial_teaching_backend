#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    project_name = "remedial_teaching"
    settings_module_name = "settings"
    if "--settings" in sys.argv:
        settings_index = sys.argv.index("--settings")
        if settings_index + 1 < len(sys.argv):
            settings_module_name = sys.argv[settings_index + 1]
            sys.argv.pop(settings_index)
        sys.argv.pop(settings_index)
    settings_module = '{project_name}.{settings_module_name}'.format(project_name=project_name, settings_module_name=settings_module_name)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
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
