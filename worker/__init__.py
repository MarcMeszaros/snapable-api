from __future__ import absolute_import
import socket
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

from celery import Celery
from django.conf import settings


if ('ares' in socket.gethostname()):
    broker = 'amqp://127.0.0.1'
elif ('athena' in socket.gethostname()):
    broker = 'amqp://127.0.0.1'
else:
    broker = 'amqp://192.168.56.102'

app = Celery(
    'worker',
    broker=broker,
    backend=broker,
    include=[
        'worker.tasks',
        'worker.event',
        'worker.passwordnonce',
    ]
)

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    celery.start()
