import api.auth
import api.utils
import api.base_v1.resources

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ALL
from tastypie.utils.mime import determine_format, build_content_type

from event import EventResource
from guest import GuestResource

from data.models import Guest

from api.utils.serializers import SnapSerializer

from data.images import SnapImage
import StringIO
from PIL import Image

class PhotoResource(api.utils.MultipartResource, api.base_v1.resources.PhotoResource):

    event = fields.ForeignKey(EventResource, 'event')
    guest = fields.ForeignKey(GuestResource, 'guest', null=True) # allow the foreign key to be null

    timestamp = fields.DateTimeField(attribute='timestamp', readonly=True, help_text='The photo timestamp. (UTC)')

    class Meta(api.base_v1.resources.PhotoResource.Meta): # set Meta to the public API Meta
        fields = api.base_v1.resources.PhotoResource.Meta.fields + ['metrics'];
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()
        serializer = SnapSerializer(formats=['json', 'jpeg'])
        filtering = dict(api.base_v1.resources.PhotoResource.Meta.filtering, **{
            'event': ['exact'],
            'streamable': ['exact'],
            'timestamp': ALL,
        })

    def dehydrate_timestamp(self, bundle):
        return bundle.data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')

    def dehydrate(self, bundle):

        # try and add the guest name
        try:
            # add the guest name as the photo name
            bundle.data['author_name'] = bundle.obj.guest.name
        except AttributeError:
            bundle.data['author_name'] = ''

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['type'] = '/private_v1/type/6/'

        return bundle

    def hydrate(self, bundle):
        # required
        if 'event' in bundle.data:
            bundle.obj.event_id = bundle.data['event']
        if 'guest' in bundle.data:
            bundle.obj.guest_id = bundle.data['guest']

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