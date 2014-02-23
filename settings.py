import os
from datetime import timedelta

# get the project path
PROJECT_PATH = os.path.dirname(__file__)

# custom import for mysql
import pymysql
pymysql.install_as_MySQLdb()

# explicitly set debug to false
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'snapabledb',            # Or path to database file if using sqlite3.
        'USER': 'snapableusr',           # Not used with sqlite3.
        'PASSWORD': 'snapable12345',     # Not used with sqlite3.
        'HOST': '192.168.56.101',        # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '***REMOVED***'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth', # Admin
    'django.contrib.messages.context_processors.messages', # Admin
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Admin
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Admin
    'django.contrib.messages.middleware.MessageMiddleware', # Admin
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware', # Adds 'Content-Length' header

    # snapable
    'api.utils.middleware.RequestLoggingMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    # core apps for snapable
    'data',
    'api',
    'admin',
    # third-party libraries/apps
    'raven.contrib.django',
    'tastypie',
    'south',

    # django related
    'grappelli',
    'django.contrib.admin',
    # required for admin
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(process)d] [%(levelname)s] %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
        'requests': {
            'format': '%(asctime)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'console.requests':{
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'requests',
        },
        'sentry': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'file.requests': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(PROJECT_PATH, 'logs', 'requests.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 14,
            'utc': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.db.backend': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'celery': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': True,
        },
        'snapable': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'snapable.deprecated': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'snapable.request': {
            'handlers': ['console.requests', 'file.requests'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# django passwords
PASSWORD_HASHERS = (
    #'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
)

##### Django 1.5+ requires this #####
AUTH_USER_MODEL = 'data.User'
ALLOWED_HOSTS = ['.snapable.com']

##### Email #####
EMAIL_BACKEND = 'api.utils.email.SnapEmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

##### RACKSPACE #####
RACKSPACE_CLOUDFILE_CONTAINER_PREFIX = 'dev_images_'
RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX = 'dev_downloads_'
RACKSPACE_CLOUDFILE_WATERMARK = 'dev_watermark'
RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER = 10000
RACKSPACE_CLOUDFILE_PUBLIC_NETWORK = True

##### Tastypie #####
API_LIMIT_PER_PAGE = 50
TASTYPIE_DEFAULT_FORMATS = ['json']
TASTYPIE_ABSTRACT_APIKEY = True

##### Stripe #####
STRIPE_KEY_SECRET = '***REMOVED***' # testing
STRIPE_KEY_PUBLIC = '***REMOVED***' # testing
STRIPE_CURRENCY = 'usd'

##### Celery #####
# Broker settings.
BROKER_URL = 'amqp://snap_api:snapable12345@192.168.56.102:5672/snap_api'

# Results backend.
CELERY_RESULT_BACKEND = 'redis://192.168.56.102/0'

# Expire tasks after a set time
CELERY_TASK_RESULT_EXPIRES = 3600 # 1h
#CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}

# List of modules to import when celery starts.
CELERY_IMPORTS = (
    'worker.event',
    'worker.passwordnonce',
)

# tasks to run on a schedule
CELERYBEAT_SCHEDULE = {
    'passwordnonce-expire-check': {
        'task': 'worker.passwordnonce.expire',
        'schedule': timedelta(minutes=15),
        #'args': (1440)
    },
}

##### Admin #####
GRAPPELLI_ADMIN_TITLE = 'Snapable'

#### Import Local Settings #####
try:
    os.path.isfile(os.path.join(PROJECT_PATH, 'settings_local.py'))
    from settings_local import *
except Exception as e:
    pass

# setup stripe
import stripe
stripe.api_key = STRIPE_KEY_SECRET

# set debug defaults
if DEBUG:
    APIKEY = {
        'key123': 'sec123',
    }
