# python
import cStringIO
import os
import random
from calendar import monthrange
from datetime import datetime, timedelta

# django/tastypie/libs
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from PIL import Image
from uuidfield import UUIDField

# snapable
import dashboard
from photo import Photo
from utils import rackspace


@python_2_unicode_compatible
class Event(models.Model):

    account = models.ForeignKey('Account', help_text='What account the event belongs to.')
    addons = models.ManyToManyField('Addon', through='EventAddon')
    cover = models.ForeignKey('Photo', related_name='+', null=True, default=None, on_delete=models.SET_NULL, blank=True, help_text='The image to use for the event cover.')

    uuid = UUIDField(auto=True, help_text='A unique identifier for the event.')
    start_at = models.DateTimeField(default=datetime.utcnow, help_text='Event start time. (UTC)')
    end_at = models.DateTimeField(default=datetime.utcnow, help_text='Event end time. (UTC)')
    tz_offset = models.IntegerField(default=0, help_text='The timezone offset (in minutes) from UTC.')
    title = models.CharField(max_length=255, help_text='Event title.')
    url = models.CharField(max_length=255, unique=True, help_text='A "short name" for the event.')
    is_public = models.BooleanField(default=True, help_text='Is the event considered "public".')
    pin = models.CharField(max_length=255, help_text='Pseudo-random PIN used for private events.')
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the event was created. (UTC)')
    is_enabled = models.BooleanField(default=True, help_text='Is the event considered "active" in the system.')
    are_photos_streamable = models.BooleanField(default=True, help_text='Should the images be streamable by default when created.')
    are_photos_watermarked = models.BooleanField(default=False, help_text='Should a watermark be applied to non-original images.')

    # virtual properties #
    # return the number of guests related to this event
    @property
    def guest_count(self):
        return self.guest_set.count()

    # return the number of photos related to this event
    @property
    def photo_count(self):
        return self.photo_set.count()

    def __str__(self):
        return u'{0} ({1})'.format(self.title, self.url)

    def __repr__(self):
        return str({
            'account': self.account,
            'are_photos_streamable': self.are_photos_streamable,
            'are_photos_watermarked': self.are_photos_watermarked,
            'created_at': self.created_at,
            'end_at': self.end_at,
            'is_enabled': self.is_enabled,
            'is_public': self.is_public,
            'pin': self.pin,
            'start_at': self.start_at,
            'title': self.title,
            'url': self.url,
            'tz_offset': self.tz_offset,
        })

    # override the save function to set defaults if required
    def save(self, *args, **kwargs):
        if not self.pin:
            self.pin = str(random.randint(1000, 9999))  # 1000~9999 (inclusive)

        return super(Event, self).save(*args, **kwargs)

        # helper functions for the image storage
    def get_watermark(self):
        """
        Get the watermark from Cloud Files.
        """
        try:
            # check the partner API account first
            if self.account.api_account is not None:
                cont = rackspace.cloud_files.get(settings.CLOUDFILES_WATERMARK_PREFIX)

                # try and get watermark image
                obj = cont.get_object('{0}.png'.format(self.account.api_account.pk))
                watermark = Image.open(cStringIO.StringIO(obj.get()))
                return watermark

            # no partner account, use the built-in Snapable watermark
            else:
                filepath_logo = os.path.join(settings.PROJECT_PATH, 'api', 'assets', 'logo.png')
                snap_watermark = Image.open(filepath_logo)
                return snap_watermark

        except rackspace.pyrax.exceptions.NoSuchObject as e:
            return None
        except rackspace.pyrax.exceptions.NoSuchContainer as e:
            return None

    def save_watermark(self, image):
        pass

    def cleanup_photos(self):
        from worker import event
        event.cleanup_photos.delay(self.pk)

    def create_zip(self):
        from worker import event
        event.create_album_zip.delay(self.pk)

    def send_invites(self, message=''):
        from worker import event
        event.email_guests.delay(self.pk, message)


#===== Admin =====#
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


#===== Admin =====#
from .location import LocationAdminInline
@admin.register(Event, site=dashboard.site)
class EventAdmin(admin.ModelAdmin):
    inlines = [LocationAdminInline]
    actions = ['cleanup_photos', 'create_event_photo_zip', 'send_event_invites']
    exclude = ['access_count', 'are_photos_watermarked']
    list_display = ['id', 'title', 'url', 'start_at', 'end_at', 'is_public', 'pin', 'photo_count', 'guest_count', 'is_enabled', 'created_at']
    #list_filter = [UpcomingEventListFilter, 'is_public', 'is_enabled', 'start_at', 'end_at']
    readonly_fields = ['id', 'pin', 'created_at']
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
    readonly_fields = ['id', 'pin', 'created_at']
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
