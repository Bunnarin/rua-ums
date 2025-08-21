from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES['default']['HOST'] = 'localhost'

STATIC_ROOT = None
STATICFILES_DIRS = [BASE_DIR / 'static']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

