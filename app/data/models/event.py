# python
import cStringIO
import os
import random
from datetime import datetime

# django/tastypie/libs
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from PIL import Image
from uuidfield import UUIDField

# snapable
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

    @property
    def zip_download_url(self):
        cdn_uri = 'http://75e4c45674cfdf4884a0-6f5bbb6cfffb706c990262906f266b0c.r28.cf1.rackcdn.com'
        if 'dev' in settings.CLOUDFILES_DOWNLOAD_PREFIX:
            cdn_uri = 'http://23e8b3af054c2e288358-8328cee55d412b3e5ad38ec5882590af.r11.cf1.rackcdn.com'

        return '{0}/{1}.zip'.format(cdn_uri, self.uuid)

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

    def create_zip(self, send_email=True):
        from worker import event
        event.create_album_zip.delay(self.pk, send_email=send_email)

    def send_invites(self, message=''):
        from worker import event
        event.email_guests.delay(self.pk, message)
