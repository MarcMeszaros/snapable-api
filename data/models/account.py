# django/tastypie/libs
from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# snapable
import dashboard
from api.models import ApiAccount


@python_2_unicode_compatible
class Account(models.Model):

    package = models.ForeignKey('Package', null=True, default=None, help_text='The active package associated with the account.')
    addons = models.ManyToManyField('Addon', through='AccountAddon')
    users = models.ManyToManyField('User', through='AccountUser')
    valid_until = models.DateTimeField(null=True, default=None, help_text='If set, the account is valid until this date (UTC). [Usually set when buying a package.]')
    api_account = models.ForeignKey(ApiAccount, null=True, default=None, blank=True, help_text='The API Account this account was created by. (None = Snapable)')

    def __str__(self):
        company = 'Snapable' if self.api_account is None else self.api_account.company
        emails = ', '.join([u.email for u in self.users.all()])
        return u'{0} - {1}'.format(company, emails)

    def __repr__(self):
        return str({
            'api_account': self.api_account,
            'package': self.package,
            'pk': self.pk,  # Primary Key is infered from Django
            'users': self.users,
            'valid_until': self.valid_until,
        })


#===== Admin =====#
from .accountuser import AccountUserAdminInline
from .event import EventAdminInline
from .order import OrderAdminInline
@admin.register(Account, site=dashboard.site)
class AccountAdmin(admin.ModelAdmin):
    inlines = [AccountUserAdminInline, EventAdminInline, OrderAdminInline]
    list_display = ['id', 'package', 'valid_until', 'api_account', 'account__users']
    readonly_fields = ['id']
    search_fields = ['api_account__company', 'users__email']
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

    def account__users(self, obj):
        return ','.join([u.email for u in obj.users.all()])
