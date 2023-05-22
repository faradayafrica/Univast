"""
ASGI config for Univast project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from decouple import config
from django.core.asgi import get_asgi_application

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

application = get_asgi_application()
