# -*- coding: utf-8 -*-
# django/tastypies/libs
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField


@python_2_unicode_compatible
class Package(models.Model):

    # the choices for the interval field
    INTERVAL_YEAR = 'year'
    INTERVAL_MONTH = 'month'
    INTERVAL_WEEK = 'week'
    INTERVAL_CHOICES = (
        (INTERVAL_YEAR, 'Year'),
        (INTERVAL_MONTH, 'Month'),
        (INTERVAL_WEEK, 'Week'),
    )

    short_name = models.CharField(max_length=255, help_text='The package short name.')
    name = models.CharField(max_length=255, help_text='The package long name.')
    amount = models.IntegerField(help_text='The package price. (CENTS)')
    is_enabled = models.BooleanField(default=True, help_text='If the package is enabled.')
    items = JSONField(help_text='The items included in the package.')
    interval = models.CharField(max_length=5, null=True, default=None, blank=True, choices=INTERVAL_CHOICES, help_text='The interval type for the package. (NULL/day/month/year)') # day, month, year
    interval_count = models.IntegerField(default=0, help_text='The interval count for the package if the interval field isn\'t null.')
    trial_period_days = models.IntegerField(default=0, help_text='How many days to offer a trial for.')

    def __str__(self):
        return u'{0} ({1}) - ${2:.2f}'.format(self.name, self.short_name, (self.amount/100.0))

    def __repr__(self):
        return str({
            'amount': self.amount,
            'interval': self.interval,
            'interval_count': self.interval_count,
            'is_enabled': self.is_enabled,
            'name': self.name,
            'short_name': self.short_name,
        })
