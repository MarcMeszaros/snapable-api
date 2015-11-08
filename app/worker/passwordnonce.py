# worker import
from __future__ import absolute_import
from worker import app

# python
from datetime import datetime, timedelta

# snapable
from data.models import PasswordNonce


@app.task
def expire(minutes=1440):
    """
    Invalidate nonces older than X minutes.
    Defaults to 1440 minutes (24 hours).
    """
    date = datetime.utcnow() - timedelta(0, minutes)
    return PasswordNonce.objects.filter(created_at__lt=date).update(is_valid=False)
