# python
from StringIO import StringIO

# django/tastypie/libs
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse

from tastypie import fields
from tastypie.exceptions import BadRequest
from tastypie.resources import ALL
from tastypie.utils.mime import determine_format, build_content_type

from PIL import Image

# snapable
import api.utils

from .meta import BaseMeta, BaseModelResource
from data.images import SnapImage
from data.models import Guest, Photo

class PhotoResource(api.utils.MultipartResource, BaseModelResource):

    event = fields.ForeignKey('api.private_v1.resources.EventResource', 'event')
    guest = fields.ForeignKey('api.private_v1.resources.GuestResource', 'guest', null=True) # allow the foreign key to be null

    created_at = fields.DateTimeField(attribute='created_at', readonly=True, help_text='The photo timestamp. (UTC)')

    # DEPRECATED
    # old "streamable" flag (2014-07-16)
    streamable = fields.BooleanField(attribute='is_streamable', default=True)

    class Meta(BaseMeta): # set Meta to the public API Meta
        queryset = Photo.objects.filter(is_archived=False).order_by('-created_at')
        fields = ['caption', 'is_streamable', 'created_at', 'metrics', 'streamable']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        filtering = {
            'event': ['exact'],
            'created_at': ALL,
            'is_streamable': ['exact'],
            # DEPRECATED
            'streamable': ['exact'],
        }

    def dehydrate(self, bundle):

        # try and add the guest name
        try:
            # add the guest name as the photo name
            bundle.data['author_name'] = bundle.obj.guest.name
        except AttributeError:
            bundle.data['author_name'] = ''

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['type'] = '/private_v1/type/6/'
        bundle.data['timestamp'] = bundle.data['created_at'].strftime('%Y-%m-%dT%H:%M:%S')

        return bundle

    def hydrate(self, bundle):
        # required
        if 'event' in bundle.data:
            bundle.obj.event_id = bundle.data['event']
        if 'guest' in bundle.data:
            bundle.obj.guest_id = bundle.data['guest']

        return bundle

    def obj_create(self, bundle, **kwargs):
        try:
            # make sure the image is in the request
            img = Image.open(StringIO(bundle.data['image'].read()))
            snapimg = SnapImage(img)
        except KeyError as key:
            raise BadRequest('Missing field: ' + str(key))

        bundle = super(PhotoResource, self).obj_create(bundle, **kwargs)
        photo = bundle.obj

        # set the value of the event streamable value
        photo.is_streamable = photo.event.are_photos_streamable
        photo.save()

        # try and watermark
        if photo.event.are_photos_watermarked == True:
            try:
                # save the image to cloudfiles
                watermark = photo.event.get_watermark()
                photo.save_image(snapimg, True, watermark=watermark)

            except Exception as e:
                # save the image to cloudfiles
                photo.save_image(snapimg, True)

        else:
            # save the image to cloudfiles
            photo.save_image(snapimg, True)

        return bundle
