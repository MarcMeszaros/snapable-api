# -*- coding: utf-8 -*-
from django.contrib import admin

# models
from ..models import Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    actions = ['send_email_invite', 'reset_email_invite_flag']
    list_display = ['id', 'email', 'name', 'is_invited', 'created_at', 'event_id', 'event_title', 'event_url']
    list_select_related = ['event']
    readonly_fields = ['id', 'created_at', 'event']
    search_fields = ['email', 'name', '=event__pk', '^event__title', '^event__url']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'email',
                'name',
                'is_invited',
                'created_at',
            ),
        }),
        ('Ownership', {
            'classes': ('collapse',),
            'fields': (
                'event',
            )
        }),
    )

    def event_id(self, object):
        return object.event.pk

    def event_title(self, object):
        return object.event.title

    def event_url(self, object):
        return object.event.url

    def send_email_invite(self, request, queryset):
        for guest in queryset.iterator():
            guest.send_email()
        self.message_user(request, "Successfully sent email.")

    def reset_email_invite_flag(self, request, queryset):
        for guest in queryset.iterator():
            guest.is_invited = False
            guest.save()
        self.message_user(request, "Successfully sent email.")
