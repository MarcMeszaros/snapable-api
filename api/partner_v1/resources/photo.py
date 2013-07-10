# python
import StringIO

# django/tastypie/libs
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse
from PIL import Image
from tastypie import fields
from tastypie.resources import ALL
from tastypie.utils.mime import determine_format, build_content_type
from tastypie.validation import Validation

# snapable
import api.auth
import api.utils
import api.base_v1.resources

from api.utils.serializers import SnapSerializer
from data.images import SnapImage
from data.models import Guest
from event import EventResource
from guest import GuestResource

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

class PhotoResource(api.utils.MultipartResource, api.base_v1.resources.PhotoResource):

    # relations
    event = fields.ForeignKey(EventResource, 'event')
    guest = fields.ForeignKey(GuestResource, 'guest', null=True) # allow the foreign key to be null

    # virtual fields
    timestamp = fields.DateTimeField(attribute='timestamp', readonly=True, help_text='The photo timestamp. (UTC)')

    class Meta(api.base_v1.resources.PhotoResource.Meta): # set Meta to the public API Meta
        fields = ['caption', 'timestamp'];
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        authentication = api.auth.DatabaseAuthentication()
        authorization = api.auth.DatabaseAuthorization()
        validation = PhotoValidation()
        serializer = SnapSerializer(formats=['json', 'jpeg'])
        filtering = dict(api.base_v1.resources.PhotoResource.Meta.filtering, **{
            'event': ['exact'],
            'timestamp': ALL,
        })

    def dehydrate(self, bundle):
        if 'image' in bundle.data:
            del bundle.data['image']
        return bundle

    def obj_create(self, bundle, **kwargs):
        bundle = super(PhotoResource, self).obj_create(bundle, **kwargs)

        # save the image to the database
        img = Image.open(StringIO.StringIO(bundle.data['image'].read()))
        snapimg = SnapImage(img)
        bundle.obj.save_image(snapimg, True)

        return bundle

    # override the response
    def create_response(self, request, bundle, response_class=HttpResponse, **response_kwargs):
        """
        Override the default create_response method.
        """

        if (request.META['REQUEST_METHOD'] == 'GET' and 'size' in request.GET):
            bundle.data['size'] = request.GET['size']

        return super(PhotoResource, self).create_response(request, bundle, response_class=response_class, **response_kwargs)