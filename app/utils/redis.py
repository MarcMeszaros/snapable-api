from __future__ import absolute_import

# django/libs
import redis

from django.conf import settings

client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
