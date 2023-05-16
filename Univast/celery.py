from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from decouple import config as env_conf

if env_conf('DJANGO_DEVELOPMENT') == 'dev':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Univast.settings.development')
elif env_conf('DJANGO_DEVELOPMENT') == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Univast.settings.production')
elif env_conf('DJANGO_DEVELOPMENT') == 'GITHUB':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Univast.settings.workflow')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Univast.settings.production')
    
# Create a Celery app
app = Celery("univast")

# Configure Celery
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()