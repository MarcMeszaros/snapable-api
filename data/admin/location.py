# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from ..models import Location


class LocationAdminInline(admin.StackedInline):
    model = Location
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                'address',
                ('lat', 'lng'),
            ),
        }),
    )
