import api.auth
import api.v1.resources
import copy

from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ALL

from package import PackageResource
from type import TypeResource
from user import UserResource

from data.models import Address
from data.models import Event
from data.models import Photo

from api.serializers import EventSerializer

class EventResource(api.v1.resources.EventResource):

    user = fields.ForeignKey(UserResource, 'user')
    package = fields.ForeignKey(PackageResource, 'package')
    type = fields.ForeignKey(TypeResource, 'type')

    Meta = api.v1.resources.EventResource.Meta # set Meta to the public API Meta
    Meta.fields += ['cover']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = Authorization()
    Meta.serializer = EventSerializer(formats=['json', 'jpeg'])
    Meta.filtering = dict(Meta.filtering, **{
        'enabled': ['exact'],
        'user': ['exact'], 
        'start': ALL,
        'end': ALL,
    })

    def __init__(self):
        api.v1.resources.EventResource.__init__(self)

    def dehydrate(self, bundle):

        # try and add address info
        try:
            # get all addresses for the event
            db_addresses = Address.objects.filter(event_id=bundle.obj.id)
            photo_count = Photo.objects.filter(event_id=bundle.obj.id).count()
            
            # add the addresses for the event
            json_addresses = []
            for obj in db_addresses:
                json_addresses.append({
                    'address': obj.address,
                    'lat': obj.lat,
                    'lng': obj.lng,
                })

            # append the addresses to the json response
            bundle.data['addresses'] = json_addresses
            # add the photo count
            bundle.data['photo_count'] = photo_count
        except ObjectDoesNotExist:
            pass

        return bundle

    def get_object_list(self, request):

        # only do the lat/lng filtering on a list get request if both values are set
        if (request.GET.has_key('lat') and request.GET.has_key('lng')):

            # 0.000001 = 0.111 m
            # 0.000001 * 450450 = 0.450449 ~ 50km
            # variance calculation
            delta = Decimal('0.450449')
            lat_lower = Decimal(request.GET['lat']) - delta
            lat_upper = Decimal(request.GET['lat']) + delta
            lng_lower = Decimal(request.GET['lng']) - delta
            lng_upper = Decimal(request.GET['lng']) + delta

            # get addresses
            addresses = Address.objects.filter(lat__gte=lat_lower, lat__lte=lat_upper, lng__gte=lng_lower, lng__lte=lng_upper)
            values = addresses.values('event_id')
            values_list = []
            for value in values:
                values_list.append(value['event_id'])

            # get events and return
            events = super(EventResource, self).get_object_list(request)
            return events.filter(pk__in=values_list)
        else:
            return super(EventResource, self).get_object_list(request)

    # override the response
    def create_response(self, request, bundle, response_class=HttpResponse, **response_kwargs):
        """
        Override the default create_response method.
        """
        if (request.META['REQUEST_METHOD'] == 'GET' and request.GET.has_key('size')):
            bundle.data['size'] = request.GET['size']

        return super(EventResource, self).create_response(request, bundle, response_class=response_class, **response_kwargs)
