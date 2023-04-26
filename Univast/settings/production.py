from Univast.settings.settings import *

DEBUG = False

SECRET_KEY = config("SECRET_KEY")

# Database Definition
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("UNIVAST_DB_NAME"),
        "USER": config("UNIVAST_DB_USER"),
        "PASSWORD": config("UNIVAST_DB_PASSWORD"),
        "HOST": config("UNIVAST_DB_HOST"),
        "PORT": config("UNIVAST_DB_PORT"),
        "OPTIONS": {"sslmode": "require"},
    },
}

# SSL Definition
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True