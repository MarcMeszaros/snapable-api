# worker import
from __future__ import absolute_import
from worker import celery

# python
from datetime import datetime, timedelta

# snapable
from data.models import PasswordNonce

@celery.task
def expire():
    delta = datetime.now() - timedelta(hours=24)
    nonces = PasswordNonce.objects.filter(valid=True, timestamp__lte=delta)
    nonces.update(valid=False)