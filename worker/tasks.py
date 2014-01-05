from __future__ import absolute_import

from worker import app
from data.models import PasswordNonce
from datetime import datetime, timedelta

@app.task
def add(x, y):
    return x + y

@app.task
# Invalidate nonces older than X minutes.
# Defaults to 1440 minutes (24 hours).
def nonce_expiry(minutes=1440):
    date = datetime.utcnow() - timedelta(0,minutes)
    return PasswordNonce.objects.filter(created_at__lt=date).update(valid=False)
