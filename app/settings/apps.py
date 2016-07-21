# -*- coding: utf-8 -*-
from .django import DEBUG

##### Django Applications #####
# Prerequisite applications
PREREQ_APPS = [
    # django related
    'grappelli',
    'django.contrib.admin',
    # required for admin
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party libraries/apps
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'tastypie',
]

DEBUG_APPS = [
]

PROJECT_APPS = [
    'data',
    'api',
    'dashboard',
]

# Final install applications
INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS
if DEBUG:
    INSTALLED_APPS += DEBUG_APPS
