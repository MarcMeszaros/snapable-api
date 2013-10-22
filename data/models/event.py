# python
import cStringIO
import os
import random

# django/tastypie/libs
import pyrax

from django.conf import settings
from django.db import models
from PIL import Image

# snapable
from data.models import Account
from data.models import Addon

class Event(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    account = models.ForeignKey(Account)
    addons = models.ManyToManyField(Addon, through='EventAddon')
    cover = models.ForeignKey('Photo', related_name='+', null=True, default=None, on_delete=models.SET_NULL, help_text='The image to use for the event cover.')

    start = models.DateTimeField(help_text='Event start time. (UTC)')
    end = models.DateTimeField(help_text='Event end time. (UTC)')
    tz_offset = models.IntegerField(default=0, help_text='The timezone offset (in minutes) from UTC.')
    title = models.CharField(max_length=255, help_text='Event title.')
    url = models.CharField(max_length=255, unique=True, help_text='A "short name" for the event.')
    public = models.BooleanField(default=True, help_text='Is the event considered "public".')
    pin = models.CharField(max_length=255, help_text='Pseudo-random PIN used for private events.')
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the event was created. (UTC)')
    last_access = models.DateTimeField(auto_now_add=True, help_text='When the event was last accessed. (UTC)')
    access_count = models.IntegerField(default=0)
    enabled = models.BooleanField(help_text='Is the event considered "active" in the system.')
    are_photos_streamable = models.BooleanField(default=True, help_text='Should the images be streamable by default when created.')
    are_photos_watermarked = models.BooleanField(default=False, help_text='Should a watermark be applied to non-original images.')

    # virtual properties #
    # return the number of photos related to this event
    def _get_photo_count(self):
        return self.photo_set.count()

    def _set_photo_count(self, value):
        pass

    # create the property
    photo_count = property(_get_photo_count, _set_photo_count)

    def __unicode__(self):
        return str({
            'account': self.account,
            'are_photos_streamable': self.are_photos_streamable,
            'are_photos_watermarked': self.are_photos_watermarked,
            'created_at': self.created_at,
            'enabled': self.enabled,
            'end': self.end,
            'pin': self.pin,
            'public': self.public,
            'start': self.start,
            'title': self.title,
            'url': self.url,
            'tz_offset': self.tz_offset,
        })

    # override the save function to set defaults if required
    def save(self, *args, **kwargs):
        if not self.pin:
            self.pin = str(random.randint(1000, 9999)) # random int between 1000 and 9999 (inclusive)

        return super(Event, self).save(*args, **kwargs)

        # helper functions for the image storage
    def get_watermark(self):
        """
        Get the watermark from Cloud Files.
        """
        try:
            # check the partner API account first
            if self.account.api_account is not None:
                conn = pyrax.connect_to_cloudfiles(public=settings.RACKSPACE_CLOUDFILE_PUBLIC_NETWORK)
                cont = conn.get_container(settings.RACKSPACE_CLOUDFILE_WATERMARK)

                # try and get watermark image
                obj = cont.get_object('{0}.png'.format(self.account.api_account.pk))
                watermark = Image.open(cStringIO.StringIO(obj.get()))
                return watermark

            # no partner account, use the built-in Snapable watermark
            else:
                filepath_logo = os.path.join(settings.PROJECT_PATH, 'api', 'assets', 'logo.png')
                snap_watermark = Image.open(filepath_logo)
                return snap_watermark

        except pyrax.exceptions.NoSuchObject as e:
            return None
        except pyrax.exceptions.NoSuchContainer as e:
            return None

    def save_watermark(self, image):
        pass
