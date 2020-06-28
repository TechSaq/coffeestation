from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

EMAIL_BACKEND = config('DJANGO_EMAIL_BACKEND',
                       default='django.core.mail.backends.console.EmailBackend')
                       
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'saquibdb',
#         'USER': 'saquib',
#         'PASSWORD': '.saqu.',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
