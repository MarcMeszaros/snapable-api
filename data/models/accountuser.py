# django/libs
from django.db import models

# snapable
import admin

class AccountUser(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    account = models.ForeignKey('Account')
    user = models.ForeignKey('User')

    is_admin = models.BooleanField(default=False, help_text='If the user is an account admin.')
    added_at = models.DateTimeField(auto_now_add=True, help_text='When the user was added to the account. (UTC)')

#===== Admin =====#
# base details for direct and inline admin models
class AccountUserAdminDetails(object):
    raw_id_fields = ['account', 'user']
    related_lookup_fields = {
        'fk': ['account', 'user'],
    }

# add the direct admin model
class AccountUserAdmin(AccountUserAdminDetails, admin.ModelAdmin):
    pass

# add the inline admin model
class AccountUserAdminInline(AccountUserAdminDetails, admin.TabularInline):
    model = AccountUser
    extra = 0