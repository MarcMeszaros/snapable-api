import cloudfiles
import StringIO
from PIL import Image

from django.conf import settings
from django.db import models

from data.images import SnapImage
from data.models import Event
from data.models import Guest
from data.models import Type

class Photo(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    # the model fields
    event = models.ForeignKey(Event)
    guest = models.ForeignKey(Guest, null=True, default=None, on_delete=models.SET_NULL)
    type = models.ForeignKey(Type)

    caption = models.CharField(max_length=255, help_text='The photo caption.')
    streamable = models.BooleanField(help_text='If the photo is streamable.')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='The photo timestamp.')
    metrics = models.TextField(help_text='JSON metrics about the photo.') # JSON metrics

    # helper functions for the image storage
    def getImage(self, size='orig'):
        """
        Get the SnapImage from Cloud Files.
        """
        if self.id != None and self.event != None:
            #connect to container
            try:
                conn = cloudfiles.Connection(settings.RACKSPACE_USERNAME, settings.RACKSPACE_APIKEY, settings.RACKSPACE_CLOUDFILE_TIMEOUT)
                cont = conn.get_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(self.event.id / 1000))

                # try an get the size wanted
                try:
                    obj = cont.get_object(str(self.event.id) + '/' + str(self.id) + '_' + size + '.jpg')
                    img = Image.open(StringIO.StringIO(obj.read()))
                    snapimg = SnapImage(img)

                    return snapimg
                except:
                    obj = cont.get_object(str(self.event.id) + '/' + str(self.id) + '_orig.jpg')
                    img = Image.open(StringIO.StringIO(obj.read()))
                    snapimg = SnapImage(img)

                    # resize the image
                    sizeList = size.split('x')
                    sizeTupple = (int(sizeList[0]), int(sizeList[1]))
                    snapimg.resize(sizeTupple)

                    # save the new photo size
                    obj = cont.create_object(str(self.event.id) + '/' + str(self.id) + '_' + size + '.jpg')
                    obj.content_type = 'image/jpeg'
                    obj.write(snapimg.img.tostring('jpeg', 'RGB'))

                    return snapimg

            except cloudfiles.errors.NoSuchObject as e:
                return None
            except cloudfiles.errors.NoSuchContainer as e:
                return None

        else:
            raise Exception('No Photo ID and/or Event ForeignKey specified.')

    def saveImage(self, image, orig=False):
        """
        Save the SnapImage to CloudFiles.
        """
        if isinstance(image, SnapImage):
            width, height = image.img.size

            # save the new photo size
            #obj = cont.create_object(str(self.event.id) + '/' + str(self.id) + '_' + size + '.jpg')
            #obj.content_type = 'image/jpeg'
            #obj.write(snapimg.img.tostring('jpeg', 'RGB'))
        else:
            raise TypeError
