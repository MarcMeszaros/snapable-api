from __future__ import absolute_import

__all__ = ['event', 'passwordnonce']

# python
import os

# libs
from celery import Celery
from django.conf import settings

# load up django settings and start the app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = Celery('worker')

# Use the config values in the Django settings file.
# Note: Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) # auto discover other tasks

if __name__ == '__main__':
    app.start()
