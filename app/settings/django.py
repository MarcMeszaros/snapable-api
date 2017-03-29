# -*- coding: utf-8 -*-
import os

import envitro
import envitro.docker

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = BASE_DIR  # deprecated

# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = envitro.str('DJANGO_SECRET_KEY')
DEBUG = envitro.bool('DJANGO_DEBUG', False)
TEMPLATE_DEBUG = DEBUG

##### Hosts/URLs #####
ALLOWED_HOSTS = ['127.0.0.1:8000', '.snapable.com'] + envitro.list('HOST_IP', [])
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

##### User #####
AUTH_USER_MODEL = 'data.User'
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
)

##### Internationalization #####
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static-www')

##### Middleware #####
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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',  # Admin
    'django.contrib.messages.context_processors.messages',  # Admin
    'django.core.context_processors.request',
)
