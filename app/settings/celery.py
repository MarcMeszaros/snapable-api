# -*- coding: utf-8 -*-
import envitro
import envitro.docker
from datetime import timedelta

from .redis import REDIS_HOST, REDIS_PORT

##### Celery #####
CELERY_BROKER_USER = envitro.str('CELERY_BROKER_USER', 'snap_api')
CELERY_BROKER_PASSWORD = envitro.str('CELERY_BROKER_PASSWORD', 'snapable12345')
CELERY_BROKER_HOST = envitro.str('CELERY_BROKER_HOST', REDIS_HOST)
CELERY_BROKER_PORT = envitro.int('CELERY_BROKER_PORT', REDIS_PORT)
CELERY_BROKER_DB = envitro.int('CELERY_BROKER_DB', 1)
CELERY_RESULT_HOST = envitro.str('CELERY_RESULT_HOST', REDIS_HOST)
CELERY_RESULT_PORT = envitro.int('CELERY_RESULT_PORT', REDIS_PORT)
CELERY_RESULT_DB = envitro.int('CELERY_RESULT_DB', 1)

# Broker/Results settings.
BROKER_URL = envitro.str('CELERY_BROKER_URL', 'redis://{0}:{1}/{2}'.format(CELERY_BROKER_HOST, CELERY_BROKER_PORT, CELERY_BROKER_DB))
CELERY_RESULT_BACKEND = envitro.str('CELERY_RESULT_URL', 'redis://{0}:{1}/{2}'.format(CELERY_RESULT_HOST, CELERY_RESULT_PORT, CELERY_RESULT_DB))

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
    },
    'update-zip-count': {
        'task': 'worker.event.update_redis_zip_counts',
        'schedule': timedelta(minutes=60),
        #'args': (1440)
    },
}
