import api.auth
import api.loggers
import api.multi
import api.v1.resources
import cloudfiles

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ALL

from event import EventResource
from guest import GuestResource
from type import TypeResource

from data.models import Guest

from api.serializers import SnapableSerializer

class PhotoResource(api.multi.MultipartResource, api.v1.resources.PhotoResource):

    event = fields.ForeignKey(EventResource, 'event')
    guest = fields.ForeignKey(GuestResource, 'guest', null=True) # allow the foreign key to be null
    type = fields.ForeignKey(TypeResource, 'type')

    Meta = api.v1.resources.PhotoResource.Meta # set Meta to the public API Meta
    Meta.fields += ['metrics']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = Authorization()
    Meta.serializer = SnapableSerializer(formats=['json', 'jpeg'])
    Meta.filtering = dict(Meta.filtering, **{
        'event': ['exact'],
    })

    def __init__(self):
        api.v1.resources.PhotoResource.__init__(self)

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

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(PhotoResource, self).obj_create(bundle, request)

        #US-based Cloud Files accounts - uncomment if your account is in the US
        conn = cloudfiles.Connection(settings.RACKSPACE_USERNAME, settings.RACKSPACE_APIKEY, settings.RACKSPACE_CLOUDFILE_TIMEOUT)

        #connect to container
        cont = None
        try:
            cont = conn.get_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(bundle.obj.event_id / 1000))
        except cloudfiles.errors.NoSuchContainer as e:
            cont = conn.create_container(settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(bundle.obj.event_id / 1000))
            api.loggers.Log.i('created a new container: ' + settings.RACKSPACE_CLOUDFILE_CONTAINER_PREFIX + str(bundle.obj.event_id / 1000))

        obj = cont.create_object(str(bundle.obj.event_id) + '/' + str(bundle.obj.id) + '_orig.jpg')
        #if the content_type is not specified the binding will attempt to guess the correct type
        obj.content_type = 'image/jpeg'
        obj.write(bundle.data['image'])

        return bundle