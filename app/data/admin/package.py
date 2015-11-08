# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from ..models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_name', 'name', 'amount', 'is_enabled']
    readonly_fields = ['id']
    search_fields = ['short_name', 'name']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'is_enabled',
                'name',
                'short_name',
                'amount',
                'items',
                ('interval', 'interval_count', 'trial_period_days'),
            ),
        }),
    )
