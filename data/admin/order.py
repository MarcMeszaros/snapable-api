# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from ..models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = ['charge', 'send_email']
    list_display = ['id', 'amount', 'amount_refunded', 'is_paid', 'coupon', 'created_at']
    #list_filter = ['is_paid', 'created_at']
    readonly_fields = ['id', 'charge_id', 'account', 'user']
    search_fields = ['coupon']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                ('charge_id', 'coupon'),
                ('amount', 'amount_refunded'),
                'items',
                'is_paid',
            ),
        }),
        ('Ownership', {
            'classes': ('collapse',),
            'fields': (
                'account',
                'user',
            )
        }),
    )

    def send_email(self, request, queryset):
        for order in queryset.iterator():
            order.send_email()

        self.message_user(request, 'Successfully sent receipt emails.')

    def charge(self, request, queryset):
        success = True
        for order in queryset.iterator():
            success = success and order.charge()

        if success:
            self.message_user(request, 'Sent charge requests')
        else:
            self.message_user(request, 'Some charges failed')


# add the inline admin model
class OrderAdminInline(admin.StackedInline):
    model = Order
    fieldsets = (
        (None, {
            'fields': (
                ('amount', 'amount_refunded', 'coupon'),
                'items',
                'is_paid',
            ),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False