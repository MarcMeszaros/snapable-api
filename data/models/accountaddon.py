from django.db import models

from data.models import Account
from data.models import Addon

class AccountAddon(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    account = models.ForeignKey(Account)
    addon = models.ForeignKey(Addon)

    quantity = models.IntegerField(default=1, help_text='The quantity modifier of the addon.')
    paid = models.BooleanField(default=False, help_text='If the event addon has been paid.')