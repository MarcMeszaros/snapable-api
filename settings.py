"""
Django settings for web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from datetime import timedelta
from utils import env_str, env_int, env_bool, docker_link_host, docker_link_port

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)
PROJECT_PATH = BASE_DIR  # deprecated

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***REMOVED***'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool('DEBUG', False)
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['127.0.0.1:8000', '.snapable.com']
if len(env_str('HOST_IP')) > 0:
    ALLOWED_HOSTS.append(env_str('HOST_IP'))

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-www')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',  # Admin
    'django.contrib.messages.context_processors.messages',  # Admin
    'django.core.context_processors.request',
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
        'NAME': env_str('DATABASE_NAME', 'snapabledb'),
        'USER': env_str('DATABASE_USER', 'snapableusr'),
        'PASSWORD': env_str('DATABASE_PASSWORD', 'snapable12345'),
        'HOST': env_str('DATABASE_HOST', docker_link_host('DB', '127.0.0.1')),
        'PORT': env_str('DATABASE_PORT', docker_link_port('DB', 3306)),
    }
}

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
            'handlers': ['console'],
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
EMAIL_HOST = env_str('EMAIL_HOST', 'smtp.mailgun.org')
EMAIL_PORT = env_int('EMAIL_PORT', 587)
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = env_str('EMAIL_HOST_USER', '***REMOVED***')
EMAIL_HOST_PASSWORD = env_str('EMAIL_HOST_PASSWORD', '***REMOVED***')

##### RACKSPACE #####
RACKSPACE_USERNAME = env_str('RACKSPACE_USERNAME', '***REMOVED***')
RACKSPACE_APIKEY = env_str('RACKSPACE_APIKEY', '***REMOVED***')
CLOUDFILES_IMAGES_PREFIX = env_str('CLOUDFILES_IMAGES_PREFIX', 'dev_images_')
CLOUDFILES_DOWNLOAD_PREFIX = env_str('CLOUDFILES_DOWNLOAD_PREFIX', 'dev_downloads_')
CLOUDFILES_WATERMARK_PREFIX = env_str('CLOUDFILES_WATERMARK_PREFIX', 'dev_watermark')
CLOUDFILES_EVENTS_PER_CONTAINER = 10000
CLOUDFILES_PUBLIC_NETWORK = env_bool('CLOUDFILES_PUBLIC_NETWORK', True)

##### Redis #####
REDIS_HOST = env_str('REDIS_HOST', docker_link_host('RD', '127.0.0.1'))
REDIS_PORT = env_int('REDIS_PORT', docker_link_port('RD', 6379))
REDIS_DB = env_int('REDIS_DB', 0)

##### Tastypie #####
API_LIMIT_PER_PAGE = 50
TASTYPIE_DEFAULT_FORMATS = ['json']
TASTYPIE_ABSTRACT_APIKEY = True
TASTYPIE_DATETIME_FORMATTING = 'iso-8601-strict'

##### Stripe #####
STRIPE_KEY_SECRET = env_str('STRIPE_KEY_SECRET', '***REMOVED***') # testing
STRIPE_KEY_PUBLIC = env_str('STRIPE_KEY_PUBLIC', '***REMOVED***') # testing
STRIPE_CURRENCY = env_str('STRIPE_CURRENCY', 'usd')

##### sendwithus #####
SENDWITHUS_KEY = env_str('SENDWITHUS_KEY', '***REMOVED***') # no email

##### Celery #####
CELERY_BROKER_USER = env_str('CELERY_BROKER_USER', 'snap_api')
CELERY_BROKER_PASSWORD = env_str('CELERY_BROKER_PASSWORD', 'snapable12345')
CELERY_BROKER_HOST = env_str('CELERY_BROKER_HOST', docker_link_host('CELERY', '127.0.0.1'))
CELERY_BROKER_PORT = env_int('CELERY_BROKER_PORT', docker_link_port('CELERY', 6379))
CELERY_RESULT_HOST = env_str('CELERY_RESULT_HOST', docker_link_host('CELERY', '127.0.0.1'))
CELERY_RESULT_PORT = env_int('CELERY_RESULT_PORT', docker_link_port('CELERY', 6379))

# Broker/Results settings.
BROKER_URL = env_str('CELERY_BROKER_URL', 'redis://{0}:{1}/1'.format(CELERY_BROKER_HOST, CELERY_BROKER_PORT))
CELERY_RESULT_BACKEND = env_str('CELERY_RESULT_URL', 'redis://{0}:{1}/1'.format(CELERY_RESULT_HOST, CELERY_RESULT_PORT))

# Celery settings
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
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

# sentry/raven
# Set your DSN value
if len(env_str('SENTRY_DSN')) > 0:
    RAVEN_CONFIG = {
        'dsn': env_str('SENTRY_DSN'),
    }

# set API keys for AJAX
APIKEY = {
    'key123': 'sec123',
}

# setup stripe
import stripe
stripe.api_key = STRIPE_KEY_SECRET

# deprecated (remove once no longer used)
RACKSPACE_CLOUDFILE_CONTAINER_PREFIX = CLOUDFILES_IMAGES_PREFIX
RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX = CLOUDFILES_DOWNLOAD_PREFIX
RACKSPACE_CLOUDFILE_WATERMARK = CLOUDFILES_WATERMARK_PREFIX
RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER = CLOUDFILES_EVENTS_PER_CONTAINER
RACKSPACE_CLOUDFILE_PUBLIC_NETWORK = CLOUDFILES_PUBLIC_NETWORK
