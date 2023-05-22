from Univast.settings.settings import *  # noqa

DEBUG = True

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

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        "LOCATION": config("REDIS_URL"), # in the format of redis://:password@host:port/db_number
        "TIMEOUT": None
    }
}

# SSL Definition
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False

# Celery settings
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")

# Cloudinary Configuration 
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
)