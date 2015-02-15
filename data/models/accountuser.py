# -*- coding: utf-8 -*-
# django/libs
from django.db import models


class AccountUser(models.Model):

    account = models.ForeignKey('Account')
    user = models.ForeignKey('User')

    is_admin = models.BooleanField(default=False, help_text='If the user is an account admin.')
    added_at = models.DateTimeField(auto_now_add=True, help_text='When the user was added to the account. (UTC)')
