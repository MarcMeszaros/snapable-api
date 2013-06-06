import os
import socket
import sys

# get the project path
PROJECT_PATH_INNER = os.path.dirname(__file__)
PROJECT_PATH = os.path.dirname(PROJECT_PATH_INNER)

# create the 'logs' folder(s) if it doesn't already exist
if not os.path.exists(os.path.join(PROJECT_PATH, 'logs')):
    os.makedirs(os.path.join(PROJECT_PATH, 'logs'))

# start newrelic if on athena (staging)
if ('athena' in socket.gethostname()):
    import newrelic.agent
    newrelic.agent.initialize('newrelic.ini', 'staging')
# start newrelic if on ares (production)
elif ('ares' in socket.gethostname()):
    import newrelic.agent
    newrelic.agent.initialize('newrelic.ini', 'production')

# Django settings for api project.
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'snapabledb',            # Or path to database file if using sqlite3.
        'USER': 'root',                  # Not used with sqlite3.
        'PASSWORD': 'snapable12345',     # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
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
STATIC_ROOT = ''

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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # snapable
    'api.utils.middleware.RequestLoggingMiddleware',
)

ROOT_URLCONF = 'api.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'api.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',

    # core apps for snapable
    'api',
    'data',
    # third-party libraries/apps
    'raven.contrib.django',
    'tastypie',
    'south',
)

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(process)d] [%(levelname)s] %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file.firehose': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(PROJECT_PATH, 'logs', 'firehose.log'),
            'when': 'D',
            'interval': 1,
            'backupCount': 14,
            'utc': True,
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
        '': {
            'handlers': ['file.firehose'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['file.firehose', 'sentry', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file.firehose', 'sentry'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backend': {
            'handlers': ['sentry'],
            'level': 'WARNING',
            'propagate': True,
        },
        'snapable': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'snapable.request': {
            'handlers': ['file.requests'],
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

# email backend
EMAIL_BACKEND = 'api.utils.email.SnapEmailBackend'

# RACKSPACE
RACKSPACE_CLOUDFILE_CONTAINER_PREFIX = 'dev_photos_'
RACKSPACE_CLOUDFILE_TIMEOUT = 120
RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER = 10000

# tastypie settings
API_LIMIT_PER_PAGE = 50
TASTYPIE_DEFAULT_FORMATS = ['json']

# import local settings
try:
    os.path.isfile(os.path.join(PROJECT_PATH, 'settings_local.py'))
    from settings_local import *
except Exception as e:
    pass

# set debug defaults
if DEBUG:
    # custom test runner
    TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'
    # what modules to exclude from the test coverage
    COVERAGE_MODULE_EXCLUDES = [
        # custom
        'raven', 'south', 'tastypie', 'api.wsgi',
        # default
        'tests$', 'settings$', 'urls$', 'locale$', 'common.views.test', '__init__', 'django', 'migrations'
    ]
    COVERAGE_REPORT_HTML_OUTPUT_DIR = 'build/reports'

    APIKEY = {
        'key123': 'sec123',
    }