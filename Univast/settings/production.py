from Univast.settings.settings import *  # noqa

DEBUG = False

SECRET_KEY = config("SECRET_KEY")  # noqa

# Database Definition
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("UNIVAST_DB_NAME"),  # noqa
        "USER": config("UNIVAST_DB_USER"),  # noqa
        "PASSWORD": config("UNIVAST_DB_PASSWORD"),  # noqa
        "HOST": config("UNIVAST_DB_HOST"),  # noqa
        "PORT": config("UNIVAST_DB_PORT"),  # noqa
        "OPTIONS": {"sslmode": "require"},  # noqa
    },
}

# SSL Definition
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

# Celery settings
CELERY_BROKER_URL = config("CELERY_BROKER_URL") + '?ssl_cert_reqs=required'
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND") + '?ssl_cert_reqs=required'
