from django.db import models

from data.models import Account
from data.models import User

class AccountUser(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    account = models.ForeignKey(Account)
    user = models.ForeignKey(User)

    admin = models.BooleanField(default=False, help_text='If the user is an account admin.')
    date_added = models.DateTimeField(auto_now_add=True, help_text='When the user was added to the account. (UTC)')