import api.auth
import api.v1.resources
import copy
import pytz

from datetime import datetime, timedelta
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
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

    Meta = api.v1.resources.EventResource.Meta # set Meta to the public API Meta
    Meta.fields += ['cover']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.ordering += ['start', 'end']
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

            # convert the "public" flag into the old type values
            if bundle.obj.public == True:
                bundle.data['type'] = '/private_v1/type/6/'
            else:
                bundle.data['type'] = '/private_v1/type/5/'

        except ObjectDoesNotExist:
            pass

        return bundle

    def hydrate(self, bundle):
        
        # convert the old type values into "public" flag 
        if bundle.data.has_key('type'):
            if bundle.data['type'] == '/private_v1/type/6/':
                bundle.obj.public = True
            else:
                bundle.obj.public = False

        return bundle

    def get_object_list(self, request):

        # only do the lat/lng filtering on a list get request if both values are set
        if (request.GET.has_key('lat') and request.GET.has_key('lng')):

            # 0.000001 = 0.111 m
            # 0.000001 * 450450 = 0.450449 ~ 50km
            # 0.000001 * 225255 = 0.225225 ~ 25km
            # 0.000001 * 90090 = 0.09009 ~ 10km
            # 0.000001 * 45045 = 0.045045 ~ 5km
            # 0.000001 * 18018 = 0.018018 ~ 2km
            # 0.000001 * 9009 = 0.009009 ~ 1km
            # variance calculation
            delta_distance = Decimal('0.225225')
            lat_lower = Decimal(request.GET['lat']) - delta_distance
            lat_upper = Decimal(request.GET['lat']) + delta_distance
            lng_lower = Decimal(request.GET['lng']) - delta_distance
            lng_upper = Decimal(request.GET['lng']) + delta_distance

            # get addresses
            addresses = Address.objects.filter(lat__gte=lat_lower, lat__lte=lat_upper, lng__gte=lng_lower, lng__lte=lng_upper)
            values = addresses.values('event_id')
            values_list = []
            for value in values:
                values_list.append(value['event_id'])

            # get base events
            events = super(EventResource, self).get_object_list(request)

            # the possible time GET params to filter on events
            possible_time_params = [
                'start', 'start__gt', 'start__gte', 'start__lt', 'start__lte',
                'end', 'end__gt', 'end__gte', 'end__lt', 'end__lte',
            ]

            # fancy algorithm to detect if there are none of the time filtering GET params
            # if there is not time filtering, apply our default time filtering
            #
            # the condition check works as follows:
            # 1. get the request param keys and turn it into a set, turn the possible params into a set
            # 2. do the intersect between both sets ('&' operator)
            # 3. convert the resulting interset into a list
            # 4. check the list length to see how many possible time filters are in the request (if 0, do our default algorithm)
            if (len(list(set(request.GET.keys()) & set(possible_time_params))) == 0):

                # query filtering variables
                delta_minutes = 24 * 60
                now_datetime = datetime.now(pytz.utc) # current time on server
                pre_now_datetime = now_datetime + timedelta(0, 0, 0, 0, -delta_minutes) # delta minutes in the past
                post_now_datetime = now_datetime + timedelta(0, 0, 0, 0, delta_minutes) # delta minutes in the future

                # default queryset filtering for events to only show events +/- delta or in progress:
                #
                #      start    end
                # -------|-------|-------> time
                #    ^       ^       ^
                #    1       2       3     possible points during an event
                #
                # delta = 24 hours
                # 1 = (start > now && start <= (now + delta))
                # 2 = (start < now && end > now)
                # 3 = (end < now && end >= (now - delta))
                #
                events = events.filter(
                    (Q(start__gt=now_datetime) & Q(start__lte=post_now_datetime)) | (Q(start__lte=now_datetime) & Q(end__gte=now_datetime)) | (Q(end__lt=now_datetime) & Q(end__gte=pre_now_datetime))
                )

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
