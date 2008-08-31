import os.path
import sys

PROJECT_ROOT = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    #('Your name', 'your@mail.com'),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_ROOT, 'btt.sqlite')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Europe/Chisinau'

LANGUAGE_CODE = 'en'
from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)
USE_I18N = True

SITE_ID = 1

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/media/'

# !!!NEW KEY REQUIRED!!!
SECRET_KEY = 'iuiuha76t7%7gya7g^&^R%^R%^R%a6s5dr5ashgvffg67%a'

APPEND_SLASH = True
PREPEND_WWW = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'blog',
)

######### Custom settings #########

# Items per page
PER_PAGE = 50

try:
    from settings_local import *
except ImportError:
    pass
