import cloudfiles
import StringIO
import tastypie.exceptions
import tastypie.http

from django.conf import settings
from tastypie.serializers import Serializer

from data.models import Photo
from data.images import SnapImage

from PIL import Image

class PhotoSerializer(Serializer):
    formats = Serializer.formats + [
        'jpeg'
    ]
    content_types = dict(Serializer.content_types, **{
        'jpeg': 'image/jpeg',
    })

    def to_jpeg(self, bundle, options=None):
        photo = bundle.obj
        event = bundle.obj.event
        size = 'orig'

        # set the size variable
        if (bundle.data != None and bundle.data.has_key('size')):
            size = bundle.data['size']

        snapimg = photo.get_image(size)
        return snapimg.img.tostring('jpeg', 'RGB')

    def from_jpeg(self, content):
        data = []
        return data

class EventSerializer(Serializer):
    formats = Serializer.formats + [
        'jpeg'
    ]
    content_types = dict(Serializer.content_types, **{
        'jpeg': 'image/jpeg',
    })

    def to_jpeg(self, bundle, options=None):
        event = bundle.obj
        size = 'orig'

        # get the photo count
        photos_count = Photo.objects.filter(event_id=event.id).count()

        # set the size variable
        if (bundle.data != None and bundle.data.has_key('size')):
            size = bundle.data['size']

        # event cover it is set
        if (event.cover != 0):
            cover_photo = Photo.objects.get(pk=event.cover)
            snapimg = cover_photo.get_image(size)

            return snapimg.img.tostring('jpeg', 'RGB')
        # there is no cover and at least one photo
        elif (event.cover == 0 and photos_count >= 1):
            first_photo = list(Photo.objects.filter(event_id=event.id).order_by('timestamp'))[0]
            snapimg = first_photo.get_image(size)

            return snapimg.img.tostring('jpeg', 'RGB')
        # no photo, no cover, return exception
        else:
            raise tastypie.exceptions.ImmediateHttpResponse(tastypie.http.HttpNotFound())

    def from_jpeg(self, content):
        data = []
        return data