from __future__ import absolute_import

from worker import celery


@celery.task
def add(x, y):
    return x + y


@celery.task
def mul(x, y):
    return x * y


@celery.task(ignore_result=True)
def xsum(numbers):
    return sum(numbers)