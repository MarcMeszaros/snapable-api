import api.auth
import api.utils
import api.base_v1.resources
import cloudfiles

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ALL
from tastypie.utils.mime import determine_format, build_content_type

from event import EventResource
from guest import GuestResource
from type import TypeResource

from data.models import Guest

from api.utils import PhotoSerializer

from data.images import SnapImage
import StringIO
from PIL import Image

class PhotoResource(api.utils.MultipartResource, api.base_v1.resources.PhotoResource):

    event = fields.ForeignKey(EventResource, 'event')
    guest = fields.ForeignKey(GuestResource, 'guest', null=True) # allow the foreign key to be null
    type = fields.ForeignKey(TypeResource, 'type')

    timestamp = fields.DateTimeField(attribute='timestamp', readonly=True, help_text='The photo timestamp. (UTC)')

    class Meta(api.base_v1.resources.PhotoResource.Meta): # set Meta to the public API Meta
        fields = api.base_v1.resources.PhotoResource.Meta.fields + ['metrics'];
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()
        serializer = PhotoSerializer(formats=['json', 'jpeg'])
        filtering = dict(api.base_v1.resources.PhotoResource.Meta.filtering, **{
            'event': ['exact'],
            'timestamp': ALL,
        })

    def dehydrate_timestamp(self, bundle):
        return bundle.data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')

    def dehydrate(self, bundle):

        # try and add the guest name
        try:
            # add the guest name as the photo name
            guest = Guest.objects.get(pk=bundle.obj.guest_id)
            bundle.data['author_name'] = guest.name
        except ObjectDoesNotExist:
            bundle.data['author_name'] = ''

        return bundle

    def hydrate(self, bundle):
        # required
        if bundle.data.has_key('event'):
            bundle.obj.event_id = bundle.data['event']
        if bundle.data.has_key('type'):
            bundle.obj.type_id = bundle.data['type']
        if bundle.data.has_key('guest'):
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

        if (request.META['REQUEST_METHOD'] == 'GET' and request.GET.has_key('size')):
            bundle.data['size'] = request.GET['size']

        return super(PhotoResource, self).create_response(request, bundle, response_class=response_class, **response_kwargs)