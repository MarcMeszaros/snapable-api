# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from .accountuser import AccountUserAdminInline
from .event import EventAdminInline
from .order import OrderAdminInline
from ..models import Account


@admin.register(Account)
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
