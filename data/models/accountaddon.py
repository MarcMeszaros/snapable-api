from django.db import models

from data.models import Addon
from data.models import Event

class AccountAddon(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    event = models.ForeignKey(Event)
    addon = models.ForeignKey(Addon)

    quantity = models.IntegerField(default=1, help_text='The quantity modifier of the addon.')
    paid = models.BooleanField(default=False, help_text='If the event addon has been paid.')