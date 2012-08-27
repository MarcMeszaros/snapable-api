import os

# create the 'logs' folder(s) if it doesn't already exist
if not os.path.exists(os.path.join(os.getcwd(), 'logs')):
    os.makedirs(os.path.join(os.getcwd(), 'logs'))
if not os.path.exists(os.path.join(os.getcwd(), 'logs', 'debug')):
    os.makedirs(os.path.join(os.getcwd(), 'logs', 'debug'))
if not os.path.exists(os.path.join(os.getcwd(), 'logs', 'info')):
    os.makedirs(os.path.join(os.getcwd(), 'logs', 'info'))
if not os.path.exists(os.path.join(os.getcwd(), 'logs', 'warning')):
    os.makedirs(os.path.join(os.getcwd(), 'logs', 'warning'))
if not os.path.exists(os.path.join(os.getcwd(), 'logs', 'error')):
    os.makedirs(os.path.join(os.getcwd(), 'logs', 'error'))
if not os.path.exists(os.path.join(os.getcwd(), 'logs', 'critical')):
    os.makedirs(os.path.join(os.getcwd(), 'logs', 'critical'))
if not os.path.exists(os.path.join(os.getcwd(), 'logs', 'firehose')):
    os.makedirs(os.path.join(os.getcwd(), 'logs', 'firehose'))

# Django settings for api project.
DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

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
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

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
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

    # various sub-apps for snapable
    'data',
    # third-party libraries/apps
    'raven.contrib.django',
    'tastypie',
    'south',
    'gunicorn',
)

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'file.firehose': {
            'level': 'WARNING',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join('logs', 'firehose', 'firehose.log'),
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file.critical': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join('logs', 'critical', 'critical.log'),
        },
        'file.error': {
            'level': 'ERROR',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join('logs', 'error', 'error.log'),
        },
        'file.warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join('logs', 'warning', 'warning.log'),
        },
        'file.info': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join('logs', 'info', 'info.log'),
        },
        'file.debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join('logs', 'debug', 'debug.log'),
        },
    },
    'loggers': {
        '': {
            'handlers': ['file.firehose', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'snapable': {
            'handlers': ['file.debug', 'file.info', 'file.warning', 'file.error', 'file.critical', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# django passwords
PASSWORD_HASHERS = (
    #'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
)

DEBUG_AUTHENTICATION = DEBUG
DEBUG_AUTHORIZATION = DEBUG

# RACKSPACE
RACKSPACE_CLOUDFILE_CONTAINER_PREFIX = 'dev_photos_'
RACKSPACE_CLOUDFILE_TIMEOUT = 60

# tastypie settings
API_LIMIT_PER_PAGE = 50

# import local settings
try:
    os.path.isfile('../settings_local.py')
    from settings_local import *
except Exception as e:
    pass

# make the debug values whatever the debug value django is after local settings are applied
TEMPLATE_DEBUG = DEBUG
TASTYPIE_FULL_DEBUG = DEBUG