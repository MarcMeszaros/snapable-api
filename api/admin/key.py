# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from ..models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'secret', 'version', 'is_enabled', 'created_at']
    readonly_fields = ['id', 'created_at']
    search_fields = ['key', 'secret']
    raw_id_fields = ['account']
    related_lookup_fields = {
        'fk': ['account', 'cover'],
    }
    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }
    fieldsets = (
        (None, {
            'fields': (
                'id',
                ('key', 'secret'),
                ('version', 'is_enabled'),
                'permission_mask',
                'created_at',
            ),
        }),
        ('Ownership', {
            'classes': ('collapse',),
            'fields': (
                'account',
            )
        }),
    )


# add the inline admin model
class ApiKeyAdminInline(admin.StackedInline):
    model = ApiKey
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                ('key', 'secret'),
                ('version', 'is_enabled'),
                'permission_mask',
            ),
        }),
    )
