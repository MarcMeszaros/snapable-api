from __future__ import absolute_import
import socket

from celery import Celery

if ('ares' in socket.gethostname()):
    broker = 'amqp://127.0.0.1'
elif ('athena' in socket.gethostname()):
    broker = 'amqp://127.0.0.1'
else:
    broker = 'amqp://192.168.56.102'

celery = Celery(
    'worker.celery',
    broker=broker,
    include=[
        'worker.tasks',
        'worker.event',
        'worker.passwordnonce',
    ]
)

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    celery.start()