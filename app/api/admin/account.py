# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from ..models import ApiAccount
from .key import ApiKeyAdminInline


@admin.register(ApiAccount)
class ApiAccountAdmin(admin.ModelAdmin):
    inlines = [ApiKeyAdminInline]
    list_display = ['id', 'email', 'company', 'created_at']
    readonly_fields = ['id', 'created_at']
    search_fields = ['email', 'company']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'email',
                'company',
                'created_at',
            ),
        }),
    )
