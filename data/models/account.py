from django.db import models

from api.models import ApiAccount

from data.models import Addon
from data.models import Package
from data.models import User

class Account(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    package = models.ForeignKey(Package, null=True, default=None, help_text='The active package associated with the account.')
    addons = models.ManyToManyField(Addon, through='AccountAddon')
    users = models.ManyToManyField(User, through='AccountUser')
    valid_until = models.DateTimeField(null=True, default=None, help_text='If set, the account is valid until this date (UTC). [Usually set when buying a package.]')
    api_account = models.ForeignKey(ApiAccount, null=True, default=None)