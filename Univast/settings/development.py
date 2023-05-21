from Univast.settings.settings import *  # noqa

DEBUG = True

SECRET_KEY = config("SECRET_KEY")  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # noqa
    }
}

# SSL Definition
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False

# Celery settings
CELERY_BROKER_URL = config("CELERY_BROKER_URL")  # noqa
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND")  # noqa

# Cloudinary Configuration
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
)
