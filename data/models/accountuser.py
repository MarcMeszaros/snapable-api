# django/libs
from django.contrib import admin
from django.db import models


class AccountUser(models.Model):

    account = models.ForeignKey('Account')
    user = models.ForeignKey('User')

    is_admin = models.BooleanField(default=False, help_text='If the user is an account admin.')
    added_at = models.DateTimeField(auto_now_add=True, help_text='When the user was added to the account. (UTC)')


#===== Admin =====#
# add the direct admin model
class AccountUserAdminInline(admin.TabularInline):
    model = AccountUser
    extra = 0
    raw_id_fields = ['account', 'user']
    related_lookup_fields = {
        'fk': ['account', 'user'],
    }
