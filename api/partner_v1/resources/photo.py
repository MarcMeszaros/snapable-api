# python
from StringIO import StringIO

# django/tastypie/libs
from PIL import Image
from tastypie import fields
from tastypie.resources import ALL
from tastypie.validation import Validation

# snapable
import api.utils

from .meta import BaseMeta, BaseModelResource
from data.images import SnapImage
from data.models import Guest, Photo

class PhotoValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        required = ['event']
        for key in required:
            try:
                bundle.data[key]
            except KeyError:
                errors[key] = 'Missing field'

        return errors

class PhotoResource(api.utils.MultipartResource, BaseModelResource):

    # relations
    event = fields.ForeignKey('api.partner_v1.resources.EventResource', 'event')
    guest = fields.ForeignKey('api.partner_v1.resources.GuestResource', 'guest', null=True) # allow the foreign key to be null

    # virtual fields
    created_at = fields.DateTimeField(attribute='created_at', readonly=True, help_text='The photo timestamp. (UTC)')

    class Meta(BaseMeta): # set Meta to the public API Meta
        queryset = Photo.objects.all().order_by('-created_at')
        fields = ['caption', 'created_at'];
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        validation = PhotoValidation()
        filtering = {
            'event': ['exact'],
            'created_at': ALL,
        }

    def dehydrate(self, bundle):
        if 'image' in bundle.data:
            del bundle.data['image']
        return bundle

    def obj_create(self, bundle, **kwargs):
        bundle = super(PhotoResource, self).obj_create(bundle, **kwargs)

        # save the image to the database
        img = Image.open(StringIO(bundle.data['image'].read()))
        snapimg = SnapImage(img)
        bundle.obj.save_image(snapimg, True)

        return bundle
