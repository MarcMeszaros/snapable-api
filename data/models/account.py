# django/tastypie/libs
from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# snapable
from api.models import ApiAccount
from data.models import Addon, Package, User

@python_2_unicode_compatible
class Account(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    package = models.ForeignKey(Package, null=True, default=None, help_text='The active package associated with the account.')
    addons = models.ManyToManyField(Addon, through='AccountAddon')
    users = models.ManyToManyField(User, through='AccountUser')
    valid_until = models.DateTimeField(null=True, default=None, help_text='If set, the account is valid until this date (UTC). [Usually set when buying a package.]')
    api_account = models.ForeignKey(ApiAccount, null=True, default=None, blank=True, help_text='The API Account this account was created by. (None = Snapable)')

    def __str__(self):
        company = 'Snapable' if self.api_account is None else self.api_account.company
        return '{0} - ({1})'.format(self.pk, company)

    def __repr__(self):
        return str({
            'api_account': self.api_account,
            'package': self.package,
            'pk': self.pk, # Primary Key is infered from Django
            'users': self.users,
            'valid_until': self.valid_until,
        })

class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'package', 'valid_until']
    readonly_fields = ['id']
    search_fields = []
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'package',
            ),
        }),
        ('Ownership', {
            'classes': ('collapse',),
            'fields': (
                'api_account',
            )
        }),
    )

admin.site.register(Account, AccountAdmin)
