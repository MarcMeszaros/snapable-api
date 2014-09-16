"""
Django settings for web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)
PROJECT_PATH = BASE_DIR  # deprecated

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***REMOVED***'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1:8000', '.snapable.com']

# Application definition
INSTALLED_APPS = (
    # core apps for snapable
    'data',
    'api',
    'dashboard',
    # third-party libraries/apps
    'raven.contrib.django.raven_compat',
    'tastypie',

    # django related
    'grappelli',
    'django.contrib.admin.apps.SimpleAdminConfig',
    # required for admin
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Admin
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Admin
    'django.contrib.messages.middleware.MessageMiddleware',  # Admin
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',  # 'Content-Length'

    # snapable
    'api.utils.middleware.RequestLoggingMiddleware',
)

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

# User
AUTH_USER_MODEL = 'data.User'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# custom import for mysql
import pymysql
pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'snapabledb',
        'USER': 'snapableusr',
        'PASSWORD': 'snapable12345',
        'HOST': '192.168.56.101',
        'PORT': '',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-www')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',  # Admin
    'django.contrib.messages.context_processors.messages',  # Admin
    'django.core.context_processors.request',
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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'console.requests': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'requests',
        },
        'sentry': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler',
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
            'level': 'ERROR',
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
        'celery.task': {
            'handlers': ['console', 'sentry'],
            'level': 'WARNING',
            'propagate': True,
        },
        'celery.worker': {
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
            'handlers': ['console.requests'],
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

##### Email #####
EMAIL_BACKEND = 'api.utils.email.SnapEmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

##### RACKSPACE #####
CLOUDFILES_IMAGES_PREFIX = 'dev_images_'
CLOUDFILES_DOWNLOAD_PREFIX = 'dev_downloads_'
CLOUDFILES_WATERMARK_PREFIX = 'dev_watermark'
CLOUDFILES_EVENTS_PER_CONTAINER = 10000
CLOUDFILES_PUBLIC_NETWORK = True

##### Redis #####
REDIS_HOST = '192.168.56.102'
REDIS_PORT = 6379
REDIS_DB = 0

##### Tastypie #####
API_LIMIT_PER_PAGE = 50
TASTYPIE_DEFAULT_FORMATS = ['json']
TASTYPIE_ABSTRACT_APIKEY = True
TASTYPIE_DATETIME_FORMATTING = 'iso-8601-strict'

##### Stripe #####
STRIPE_KEY_SECRET = '***REMOVED***'  # testing
STRIPE_KEY_PUBLIC = '***REMOVED***'  # testing
STRIPE_CURRENCY = 'usd'

##### sendwithus #####
SENDWITHUS_KEY = '***REMOVED***'  # no email

##### Celery #####
# Broker settings.
BROKER_URL = 'amqp://snap_api:snapable12345@192.168.56.102:5672/snap_api'

# Results backend.
CELERY_RESULT_BACKEND = 'redis://192.168.56.102/0'

# Expire tasks after a set time
CELERY_TASK_RESULT_EXPIRES = 3600  # 1h
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
    }
}

##### Admin #####
GRAPPELLI_ADMIN_TITLE = 'Snapable'

# set API keys for AJAX
APIKEY = {
    'key123': 'sec123',
}

#### Import Local Settings #####
try:
    os.path.isfile(os.path.join(BASE_DIR, 'settings_local.py'))
    from settings_local import *
except Exception as e:
    pass

# setup stripe
import stripe
stripe.api_key = STRIPE_KEY_SECRET

# deprecated (remove once no longer used)
RACKSPACE_CLOUDFILE_CONTAINER_PREFIX = CLOUDFILES_IMAGES_PREFIX
RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX = CLOUDFILES_DOWNLOAD_PREFIX
RACKSPACE_CLOUDFILE_WATERMARK = CLOUDFILES_WATERMARK_PREFIX
RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER = CLOUDFILES_EVENTS_PER_CONTAINER
RACKSPACE_CLOUDFILE_PUBLIC_NETWORK = CLOUDFILES_PUBLIC_NETWORK
