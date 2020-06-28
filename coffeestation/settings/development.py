from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


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
