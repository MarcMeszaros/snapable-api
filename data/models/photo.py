# python
import cStringIO

# django/tastypie/libs
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from PIL import Image

# snapable
from data.images import SnapImage
from data.models import Event, Guest
from utils import rackspace
from utils.loggers import Log

@python_2_unicode_compatible
class Photo(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    # the model fields
    event = models.ForeignKey(Event, help_text='The event the photo belongs to.')
    guest = models.ForeignKey(Guest, null=True, default=None, on_delete=models.SET_NULL, blank=True, help_text='The guest who took the photo.')

    caption = models.CharField(max_length=255, blank=True, help_text='The photo caption.')
    streamable = models.BooleanField(default=True, help_text='If the photo is streamable.')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text='The photo timestamp.')
    metrics = models.TextField(help_text='JSON metrics about the photo.') # JSON metrics

    ## virtual properties getters/setters ##
    # return the created at timestamp
    def _get_timestamp(self):
        Log.deprecated('Photo.timestamp is deprecated. Use Photo.created_at', stacklevel=2)
        return self.created_at

    def _set_timestamp(self, value):
        Log.deprecated('Photo.timestamp is deprecated. Use Photo.created_at', stacklevel=2)
        self.created_at = value

    # add the virtual properties
    timestamp = property(_get_timestamp, _set_timestamp)

    def __str__(self):
        return '{0} - <{1}> {2}'.format(self.pk, self.event, self.caption)

    def __repr__(self):
        return str({
            'caption': self.caption,
            'created_at': self.created_at,
            'event': self.event,
            'metrics': self.metrics,
            'streamable': self.streamable,
        })

    # override built-in delete function
    def delete(self):
        cont = rackspace.cloud_files.get_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(self.event.id / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))

        # get all files related to this photo (original + resizes)
        images = cont.get_objects(prefix='{0}/{1}_'.format(self.event.id, self.id))

        # loop through the list and delete them
        for image in images:
            cont.delete_object(image)

        # delete the model as usual
        super(Photo, self).delete()

    # helper functions for the image storage
    def get_image(self, size='orig'):
        """
        Get the SnapImage from Cloud Files.
        """
        if self.id != None and self.event != None:
            #connect to container
            try:
                cont = rackspace.cloud_files.get_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(self.event.id / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))

                # try an get the size wanted
                try:
                    obj = cont.get_object('{0}/{1}_{2}.jpg'.format(self.event.id, self.id, size))
                    img = Image.open(cStringIO.StringIO(obj.get()))
                    snapimg = SnapImage(img)

                    return snapimg
                except:
                    try:
                        obj = cont.get_object('{0}/{1}_crop.jpg'.format(self.event.id, self.id))
                        img = Image.open(cStringIO.StringIO(obj.get()))
                        snapimg = SnapImage(img)
                    except rackspace.pyrax.exceptions.NoSuchObject as e:
                        obj = cont.get_object('{0}/{1}_orig.jpg'.format(self.event.id, self.id))
                        img = Image.open(cStringIO.StringIO(obj.get()))
                        snapimg = SnapImage(img)
                        snapimg.crop_square()
                        obj = cont.store_object('{0}/{1}_crop.jpg'.format(self.event.id, self.id), snapimg.img.tobytes('jpeg', 'RGB'))

                    # resize the image
                    sizeList = size.split('x')
                    sizeTupple = (int(sizeList[0]), int(sizeList[1]))
                    snapimg.resize(sizeTupple)

                    # save the new photo size
                    obj = cont.store_object('{0}/{1}_{2}.jpg'.format(self.event.id, self.id, size), snapimg.img.tobytes('jpeg', 'RGB'))
                    return snapimg

            except rackspace.pyrax.exceptions.NoSuchObject as e:
                return None
            except rackspace.pyrax.exceptions.NoSuchContainer as e:
                return None

        else:
            raise Exception('No Photo ID and/or Event ForeignKey specified.')

    def save_image(self, image, orig=False, watermark=False):
        """
        Save the SnapImage to CloudFiles.
        """
        cont = None
        try:
            cont = rackspace.cloud_files.get_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(self.event.id / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
        except rackspace.pyrax.exceptions.NoSuchContainer as e:
            cont = rackspace.cloud_files.create_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(self.event.id / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))
            Log.i('created a new container: ' + settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(self.event.id / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))

        if orig == False:
            width, height = image.img.size
            size = '{0}x{1}'.format(width, height)
            try:
                # check the image color mode (convert to RGB as required)
                if image.mode == 'RGB':
                    obj = cont.store_object('{0}/{1}_{2}.jpeg'.format(self.event.id, self.id, size), image.img.tobytes('jpeg', 'RGB'))
                else:
                    obj = cont.store_object('{0}/{1}_{2}.jpeg'.format(self.event.id, self.id, size), image.img.convert('RGB').tobytes('jpeg', 'RGB'))
            except pyrax.exceptions.NoSuchContainer as e:
                return None
        else:
            try:
                # check the image color mode (convert to RGB as required)
                if image.mode == 'RGB':
                    obj = cont.store_object('{0}/{1}_orig.jpg'.format(self.event.id, self.id), image.img.tobytes('jpeg', 'RGB'))
                else:
                    obj = cont.store_object('{0}/{1}_orig.jpg'.format(self.event.id, self.id), image.img.convert('RGB').tobytes('jpeg', 'RGB'))
                image.crop_square()

                # add watermark as required to the crop version
                if watermark is not None and watermark != False:
                    image.watermark(watermark)

                # save the image
                # check the image color mode (convert to RGB as required)
                if image.mode == 'RGB':
                    obj = cont.store_object('{0}/{1}_crop.jpg'.format(self.event.id, self.id), image.img.tobytes('jpeg', 'RGB'))
                else:
                    obj = cont.store_object('{0}/{1}_crop.jpg'.format(self.event.id, self.id), image.img.convert('RGB').tobytes('jpeg', 'RGB'))
            except rackspace.pyrax.exceptions.NoSuchContainer as e:
                return None

class PhotoAdmin(admin.ModelAdmin):
    exclude = ['metrics']

admin.site.register(Photo, PhotoAdmin)

