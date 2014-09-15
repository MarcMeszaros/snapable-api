# django/libs
from django.db import models


class EventAddon(models.Model):

    event = models.ForeignKey('Event')
    addon = models.ForeignKey('Addon')

    quantity = models.IntegerField(default=1, help_text='The quantity modifier of the addon.')
    is_paid = models.BooleanField(default=False, help_text='If the event addon has been paid.')