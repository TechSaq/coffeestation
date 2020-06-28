from .base import *

import django_heroku

DEBUG = config('DEBUG', cast=bool)


INSTALLED_APPS += [
    'storages',
]

MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',
                            }
AWS_LOCATION = 'static'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'coffeestation.storage_backends.MediaStorage'

SECURE_SSL_REDIRECT = True
SECURE_SSL_EXEMPT = []
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLIC = 'same-origin'


ALLOWED_HOSTS = ['coffeestation.herokuapp.com']


django_heroku.settings(locals())
