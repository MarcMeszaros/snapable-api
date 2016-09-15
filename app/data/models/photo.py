# -*- coding: utf-8 -*-
# python
import cStringIO

# django/tastypie/libs
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from PIL import Image

# snapable
from data.images import SnapImage
from utils import rackspace
from utils.loggers import Log


class PhotoManager(models.Manager):

    def get_queryset(self):
        return super(PhotoManager, self).get_queryset().filter(is_archived=False)


@python_2_unicode_compatible
class Photo(models.Model):

    # the model fields
    event = models.ForeignKey('Event', help_text='The event the photo belongs to.')
    guest = models.ForeignKey('Guest', null=True, default=None, on_delete=models.SET_NULL, blank=True, help_text='The guest who took the photo.')

    caption = models.CharField(max_length=255, blank=True, help_text='The photo caption.')
    is_streamable = models.BooleanField(default=True, help_text='If the photo is streamable.')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, help_text='The photo timestamp.')
    is_archived = models.BooleanField(default=False, help_text='If the photo is archived.')

    def __str__(self):
        return u'{0} ({1})'.format(self.caption, self.event.url)

    def __repr__(self):
        return str({
            'caption': self.caption,
            'created_at': self.created_at,
            'event': self.event,
            'is_streamable': self.is_streamable,
        })

    def _container_name(self):
        return '{0}{1}'.format(settings.CLOUDFILES_IMAGES_PREFIX, (self.event.id / settings.CLOUDFILES_EVENTS_PER_CONTAINER))

    def _image_prefix(self):
        return '{0}/{1}_'.format(self.event.id, self.id)

    def _image_name(self, size='orig'):
        return '{0}{1}.jpg'.format(self._image_prefix(), size)

    # cleanup image resize files
    def cleanup_resizes(self):
        cont = rackspace.cloud_files.get(self._container_name())

        # get all files related to this photo (original + resizes)
        images = cont.get_objects(prefix=self._image_prefix())

        # loop through the list and delete them unless in ignore
        ignore_sizes = ['orig', 'crop']
        for image in images:
            image_name = image.name.replace(self._image_prefix(), '').replace('.jpg', '')
            if image_name not in ignore_sizes:
                cont.delete_object(image)

    # override built-in delete function
    def delete(self):
        cont = rackspace.cloud_files.get(self._container_name())

        # get all files related to this photo (original + resizes)
        images = cont.list(prefix=self._image_prefix())

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
        if self.id and self.event:
            #connect to container
            try:
                cont = rackspace.cloud_files.get(self._container_name())

                # try an get the size wanted
                try:
                    obj = cont.get_object(self._image_name(size))
                    img = Image.open(cStringIO.StringIO(obj.get()))
                    snapimg = SnapImage(img)

                    return snapimg
                except:
                    try:
                        obj = cont.get_object(self._image_name('crop'))
                        img = Image.open(cStringIO.StringIO(obj.get()))
                        snapimg = SnapImage(img)
                    except rackspace.pyrax.exceptions.NoSuchObject as e:
                        obj = cont.get_object(self._image_name('crop'))
                        img = Image.open(cStringIO.StringIO(obj.get()))
                        snapimg = SnapImage(img)
                        snapimg.crop_square()
                        obj = cont.store_object(self._image_name('crop'), snapimg.img.tobytes('jpeg', 'RGB'))

                    # resize the image
                    sizeList = size.split('x')
                    sizeTupple = (int(sizeList[0]), int(sizeList[1]))
                    snapimg.resize(sizeTupple)

                    # save the new photo size
                    obj = cont.store_object(self._image_name(size), snapimg.img.tobytes('jpeg', 'RGB'))
                    return snapimg

            except rackspace.pyrax.exceptions.NoSuchObject as e:
                if size == 'orig':
                    Log.i('No original photo. Archiving photo: {}'.format(self.id))
                    self.is_archived = True
                    self.save()
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
            cont = rackspace.cloud_files.get(self._container_name())
        except rackspace.pyrax.exceptions.NoSuchContainer as e:
            cont = rackspace.cloud_files.create(self._container_name())
            Log.i('created a new container: ' + self._container_name())

        if not orig:
            width, height = image.img.size
            size = '{0}x{1}'.format(width, height)
            try:
                # check the image color mode (convert to RGB as required)
                if image.mode == 'RGB':
                    obj = cont.store_object(self._image_name(size), image.img.tobytes('jpeg', 'RGB'))
                else:
                    obj = cont.store_object(self._image_name(size), image.img.convert('RGB').tobytes('jpeg', 'RGB'))
            except pyrax.exceptions.NoSuchContainer as e:
                return None
        else:
            try:
                # check the image color mode (convert to RGB as required)
                if image.mode == 'RGB':
                    obj = cont.store_object(self._image_name(), image.img.tobytes('jpeg', 'RGB'))
                else:
                    obj = cont.store_object(self._image_name(), image.img.convert('RGB').tobytes('jpeg', 'RGB'))
                image.crop_square()

                # add watermark as required to the crop version
                if watermark:
                    image.watermark(watermark)

                # save the image
                # check the image color mode (convert to RGB as required)
                if image.mode == 'RGB':
                    obj = cont.store_object(self._image_name('crop'), image.img.tobytes('jpeg', 'RGB'))
                else:
                    obj = cont.store_object(self._image_name('crop'), image.img.convert('RGB').tobytes('jpeg', 'RGB'))
            except rackspace.pyrax.exceptions.NoSuchContainer as e:
                return None
