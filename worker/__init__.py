from __future__ import absolute_import
import socket
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from celery import Celery
from django.conf import settings


# TODO move into settings (http://docs.celeryproject.org/en/latest/configuration.html#conf-broker-settings)
if ('ares' in socket.gethostname()):
    broker = 'amqp://snap_api:snapable12345@127.0.0.1/snap_api'
elif ('athena' in socket.gethostname()):
    broker = 'amqp://snap_api:snapable12345@127.0.0.1/snap_api'
else:
    broker = 'amqp://snap_api:snapable12345@192.168.56.102/snap_api'

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
