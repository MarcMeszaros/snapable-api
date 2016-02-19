# -*- coding: utf-8 -*-
from calendar import monthrange
from datetime import datetime, timedelta
from django.contrib import admin
from django.db.models import Q

# models
from .location import LocationAdminInline
from ..models import Event, Photo


class UpcomingEventListFilter(admin.SimpleListFilter):
    title = 'Upcoming'
    parameter_name = 'upcoming'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('any', 'Any'),
            ('today', 'Today'),
            ('week', 'Next 7 days'),
            ('month', 'This month'),
            ('year', 'This year'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        tolerance = timedelta(hours=6)
        now = datetime.utcnow()
        start = now - tolerance

        if self.value() is None:
            return queryset

        if self.value() == 'any':
            return queryset.filter(Q(start_at__gte=start) | Q(end_at__gte=start))

        if self.value() == 'today':
            end = now.replace(hour=23, minute=59, second=59)
            end += tolerance

        if self.value() == 'week':
            end = now.replace(hour=23, minute=59, second=59)
            end += timedelta(days=7) + tolerance

        if self.value() == 'month':
            end = now.replace(day=monthrange(now.year, now.month)[1], hour=23, minute=59, second=59)
            end += tolerance

        if self.value() == 'year':
            end = now.replace(month=12, day=monthrange(now.year, 12)[1], hour=23, minute=59, second=59)
            end += tolerance

        # the actual query
        query = (Q(start_at__gte=start) | Q(end_at__gte=start)) & (Q(start_at__lte=end) | Q(end_at__lte=end))
        return queryset.filter(query)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [LocationAdminInline]
    actions = ['cleanup_photos', 'create_event_photo_zip', 'send_event_invites']
    exclude = ['access_count', 'are_photos_watermarked']
    list_display = ['id', 'title', 'url', 'start_at', 'end_at', 'is_public', 'pin', 'photo_count', 'guest_count', 'is_enabled', 'created_at']
    list_filter = [UpcomingEventListFilter, 'is_public', 'is_enabled', 'start_at', 'end_at']
    readonly_fields = ['id', 'pin', 'created_at', 'zip_download_url']
    search_fields = ['title', 'url']
    raw_id_fields = ['account', 'cover']
    related_lookup_fields = {
        'fk': ['account', 'cover'],
    }
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'title',
                'url',
                ('start_at', 'end_at', 'tz_offset'),
                ('cover', 'is_public', 'are_photos_streamable'),
                ('pin', 'created_at'),
                'zip_download_url',
            ),
        }),
        ('Ownership', {
            'classes': ('collapse',),
            'fields': (
                'account',
            )
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        try:
            object_id = filter(None, request.path.split('/'))[-1]
            event = Event.objects.get(pk=object_id)
            if db_field.name == 'cover':
                kwargs['queryset'] = Photo.objects.filter(event=event)
            return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        except ValueError:
            if db_field.name == 'cover':
                kwargs['queryset'] = Photo.objects.none()
            return super(EventAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def cleanup_photos(self, request, queryset):
        for event in queryset.iterator():
            event.cleanup_photos()
        self.message_user(request, 'Successfully schedule photo cleanup.')

    def create_event_photo_zip(self, request, queryset):
        for event in queryset.iterator():
            event.create_zip()
        self.message_user(request, 'Successfully scheduled zip archive creation.')

    def send_event_invites(self, request, queryset):
        for event in queryset.iterator():
            event.send_invites()
        self.message_user(request, 'Successfully sent the event invites.')


# add the inline admin model
class EventAdminInline(admin.StackedInline):
    model = Event
    extra = 1
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'url',
                ('start_at', 'end_at', 'tz_offset'),
                ('is_public', 'are_photos_streamable'),
            ),
        }),
    )
