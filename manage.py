#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from decouple import config


def main():
    """Run administrative tasks."""
    
    if config('DJANGO_DEVELOPMENT') == 'dev':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Univast.settings.development')
    elif config('DJANGO_DEVELOPMENT') == 'prod':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Univast.settings.production')
    elif config('DJANGO_DEVELOPMENT') == 'staging':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Univast.settings.staging')
    elif config('DJANGO_DEVELOPMENT') == 'GITHUB':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Univast.settings.workflow')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Univast.settings.production')
    
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
