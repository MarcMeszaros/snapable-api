# django/tastypies/libs
from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

@python_2_unicode_compatible
class Package(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

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
    enabled = models.BooleanField(help_text='If the package is enabled.')
    items = JSONField(help_text='The items included in the package.')
    interval = models.CharField(max_length=5, null=True, choices=INTERVAL_CHOICES, default=None, help_text='The interval type for the package. (NULL/day/month/year)') # day, month, year
    interval_count = models.IntegerField(default=0, help_text='The interval count for the package if the interval field isn\'t null.')
    trial_period_days = models.IntegerField(default=0, help_text='How many days to offer a trial for.')

    def __str__(self):
        return '{0} - {1} ({2:.2f})'.format(self.pk, self.short_name, (self.amount/100.0))

    def __repr__(self):
        return str({
            'amount': self.amount,
            'enabled': self.enabled,
            'interval': self.interval,
            'interval_count': self.interval_count,
            'name': self.name,
            'short_name': self.short_name,
        })

class PackageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Package, PackageAdmin)
