# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from ..models import AccountUser


class AccountUserAdminInline(admin.TabularInline):
    model = AccountUser
    extra = 0
    raw_id_fields = ['account', 'user']
    related_lookup_fields = {
        'fk': ['account', 'user'],
    }
