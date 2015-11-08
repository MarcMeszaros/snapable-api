# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from .accountuser import AccountUserAdminInline
from ..models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [AccountUserAdminInline]
    list_display = ['id', 'email', 'first_name', 'last_name', 'created_at']
    readonly_fields = ['id', 'created_at', 'last_login']
    search_fields = ['email', 'first_name', 'last_name']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'email',
                'password',
                ('first_name', 'last_name'),
                ('last_login', 'created_at'),
            ),
            'description': '<strong>NOTE: <em>A "plaintext" password in the "password" field will be hashed and saved and will overwrite the existing password.</em></strong>'
        }),
        ('Stripe', {
            'classes': ('collapse',),
            'fields': (
                'payment_gateway_user_id',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.password[:14] != 'pbkdf2_sha256$':
            obj.set_password(obj.password)
        obj.save()
