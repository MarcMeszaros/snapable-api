# python
import copy
import itertools

from datetime import datetime, timedelta
from decimal import Decimal

# django/tastypie/libs
import pytz
import pyrax

from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.http import HttpResponse, Http404
from tastypie import fields, http
from tastypie.resources import ALL

# snapable
import settings

from .meta import BaseMeta, BaseModelResource
from data.models import Event, Location, Photo, User
from worker import app, event

class EventResource(BaseModelResource):

    # relations
    account = fields.ForeignKey('api.private_v1.resources.AccountResource', 'account', help_text='Account resource')
    addons = fields.ManyToManyField('api.private_v1.resources.EventAddonResource', 'eventaddon_set', null=True, full=True)
    addresses = fields.ToManyField('api.private_v1.resources.AddressResource', 'location_set', null=True, full=True)
    cover = fields.ForeignKey('api.private_v1.resources.PhotoResource', 'cover', null=True)

    # virtual fields
    photo_count = fields.IntegerField(attribute='photo_count', readonly=True, help_text='The number of photos for the event.')

    # DEPRECATED
    # old "enabled" flag (2013-10-22)
    enabled = fields.BooleanField(attribute='is_enabled')
    # old start/end date (2013-10-22)
    start = fields.DateTimeField(attribute='start_at')
    end = fields.DateTimeField(attribute='end_at')

    class Meta(BaseMeta): # set Meta to the public API Meta
        queryset = Event.objects.all()
        fields = [
            'start_at', 
            'end_at', 
            'tz_offset', 
            'title', 
            'url', 
            'pin', 
            'is_enabled', 
            'is_public', 
            'uuid', 
            'created_at', 
            'cover', 
            'photo_count', 
            'are_photos_streamable',
            # DEPRECATED
            'enabled', 
            'start', 
            'end'
        ]
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        zip_allowed_methods = ['get','post']
        invites_allowed_methods = ['post']
        ordering = ['start_at', 'end_at', 'start', 'end'] # DEPRECATED: start, end
        filtering = {
            'is_enabled': ['exact'],
            'account': ['exact'],
            'start_at': ALL,
            'end_at': ALL,
            'photo_count': ['gte'],
            'title': ALL,
            'url': ALL,
            # deprecated (2013-10-22)
            'enabled': ['exact'],
            'start': ALL,
            'end': ALL,
        }

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/search/$' % self._meta.resource_name, self.wrap_view('get_search'), name="api_get_search"),
            url(r'^(?P<resource_name>%s)/(?P<pk>\d+)/zip/$' % self._meta.resource_name, self.wrap_view('dispatch_zip'), name="api_dispatch_zip"),
            url(r'^(?P<resource_name>%s)/(?P<pk>\d+)/invites/$' % self._meta.resource_name, self.wrap_view('dispatch_invites'), name="api_dispatch_invites"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        delta_minutes = 24 * 60
        now_datetime = datetime.now(pytz.utc) # current time on server
        pre_now_datetime = now_datetime + timedelta(0, 0, 0, 0, -delta_minutes) # delta minutes in the past
        post_now_datetime = now_datetime + timedelta(0, 0, 0, 0, delta_minutes) # delta minutes in the future
        # query set with only events that aren't finished
        sqs = Event.objects.filter(
            (Q(title__icontains=request.GET.get('q', '')) | Q(url__icontains=request.GET.get('q', ''))) & Q(end_at__gte=pre_now_datetime)
        )
        # second query set without events that have finished
        sqs2 = Event.objects.filter(
            (Q(title__icontains=request.GET.get('q', '')) | Q(url__icontains=request.GET.get('q', ''))) & Q(end_at__lt=pre_now_datetime)
        )

        # get the union
        sorted_objects = self.apply_sorting(sqs, options=request.GET)
        sorted_objects2 = self.apply_sorting(sqs2, options=request.GET)

        # union of both query sets into a list one after the other
        result_objects = list(itertools.chain(sorted_objects, sorted_objects2))

        paginator = self._meta.paginator_class(request.GET, result_objects)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [self.build_bundle(obj=obj, request=request) for obj in result_objects]
        to_be_serialized['objects'] = [self.full_dehydrate(bundle) for bundle in bundles]

        return self.create_response(request, to_be_serialized)

    def dispatch_zip(self, request, **kwargs):
        return self.dispatch('zip', request, **kwargs)

    def dispatch_invites(self, request, **kwargs):
        return self.dispatch('invites', request, **kwargs)

    def post_zip(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            event_obj = Event.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")
        else:
            # check if there's already a job running that is creating an album archive
            if app.backend.get('event:{0}:create_album_zip'.format(kwargs['pk'])):
                http409 = http.HttpResponse
                http409.status_code = 409
                return http409()
            else:
                event.create_album_zip.delay(kwargs['pk'])
                return http.HttpAccepted()

    def get_zip(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            event_obj = Event.objects.get(pk=kwargs['pk'])

            conn = pyrax.connect_to_cloudfiles(public=settings.RACKSPACE_CLOUDFILE_PUBLIC_NETWORK)
            cont = conn.get_container(settings.RACKSPACE_CLOUDFILE_DOWNLOAD_CONTAINER_PREFIX + str(event_obj.pk / settings.RACKSPACE_CLOUDFILE_EVENTS_PER_CONTAINER))

            zip_cdn_url = cont.cdn_uri + "/" + str(event_obj.uuid) + ".zip"
            album_zip = cont.get_object(str(event_obj.uuid) + ".zip")

            response_body = {
                'zip_url': zip_cdn_url,
                'created_at': album_zip.last_modified + "Z",
            }

            return self.create_response(request, response_body)

        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except pyrax.exceptions.NoSuchContainer:
            return http.HttpNotFound()
        except pyrax.exceptions.NoSuchObject:
            return http.HttpNotFound()


    def post_invites(self, request, **kwargs):
        ### start copied from tasytpie ###
        if django.VERSION >= (1, 4):
            body = request.body
        else:
            body = request.raw_post_data
        deserialized = self.deserialize(request, body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        ## start custom code ##
        try:
            event_obj = Event.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")
        else:
            event.email_guests.delay(kwargs['pk'], bundle.data['message'])
            return http.HttpAccepted()

    def apply_filters(self, request, applicable_filters):
        # check if the filter is there
        if 'photo_count__gte' in applicable_filters:
            custom = applicable_filters.pop('photo_count__gte')
        else:
            custom = None

        # inital filtering
        semi_filtered = super(EventResource, self).apply_filters(request, applicable_filters)

        # do our custom filtering
        if custom:
            semi_filtered = filter(lambda x: x.photo_count >= int(custom), list(semi_filtered))

        return semi_filtered

    def dehydrate(self, bundle):
        try:
            ### DEPRECATED/COMPATIBILITY ###
            # old start/end date (2013-10-22)
            bundle.data['start'] = bundle.obj.start_at.strftime('%Y-%m-%dT%H:%M:%S')
            bundle.data['end'] = bundle.obj.end_at.strftime('%Y-%m-%dT%H:%M:%S')

            # convert the "enabled" flag (2013-10-22)
            bundle.data['enabled'] = bundle.obj.is_enabled

            # convert the "public" flag (2013-10-22)
            bundle.data['public'] = bundle.obj.is_public

            # add the old user field
            users = User.objects.filter(account=bundle.obj.account, accountuser__is_admin=True)
            if users.count() > 0:
                bundle.data['user'] = '/private_v1/user/{0}/'.format(users[0].pk)
            else:
                bundle.data['user'] = ''

            # add the old package field
            if bundle.obj.account.package:
                bundle.data['package'] = '/private_v1/package/{0}/'.format(bundle.obj.account.package.pk)
            else:
                bundle.data['package'] = '/private_v1/package/1/'

            # convert the "public" flag into the old type values
            if bundle.obj.is_public == True:
                bundle.data['type'] = '/private_v1/type/6/'
            else:
                bundle.data['type'] = '/private_v1/type/5/'

            # add the old 'creation_date'/'created' field
            bundle.data['creation_date'] = bundle.data['created_at']
            bundle.data['created'] = bundle.data['created_at']

        except ObjectDoesNotExist:
            pass

        return bundle

    def dehydrate_end_at(self, bundle):
        return bundle.data['end_at'].strftime('%Y-%m-%dT%H:%M:%SZ')

    def dehydrate_start_at(self, bundle):
        return bundle.data['start_at'].strftime('%Y-%m-%dT%H:%M:%SZ')

    def hydrate(self, bundle):
        ### DEPRECATED/COMPATIBILITY ###
        # convert the old type "public" flag (2013-10-22)
        if 'public' in bundle.data:
            bundle.obj.is_public = bundle.data['public']

        # convert the old type values into "public" flag
        if 'type' in bundle.data:
            if bundle.data['type'] == '/private_v1/type/6/':
                bundle.obj.is_public = True
            else:
                bundle.obj.is_public = False
        # convert cover into a resource link
        if 'cover' in bundle.data and type(bundle.data['cover']) == int:
            bundle.obj.cover = Photo.objects.get(pk=bundle.data['cover'])

        return bundle

    def get_object_list(self, request):

        # only do the lat/lng filtering on a list get request if both values are set
        if ('lat' in request.GET and 'lng' in request.GET):

            # [(distance(m) / 0.111) * 0.000001] = ratio delta
            # ie: [(25000 / 0.111) * 0.000001] = 0.225225 ~ 25km
            #
            # 0.000001 = 0.111 m
            # 0.000001 * 225255 = 0.225225 ~ 25km
            # 0.000001 * 90090 = 0.09009 ~ 10km
            # 0.000001 * 45045 = 0.045045 ~ 5km
            # 0.000001 * 18018 = 0.018018 ~ 2km
            # 0.000001 * 9009 = 0.009009 ~ 1km
            # variance calculation
            delta_distance = Decimal('0.09009')
            lat_lower = Decimal(request.GET['lat']) - delta_distance
            lat_upper = Decimal(request.GET['lat']) + delta_distance
            lng_lower = Decimal(request.GET['lng']) - delta_distance
            lng_upper = Decimal(request.GET['lng']) + delta_distance

            # get addresses
            addresses = Location.objects.filter(lat__gte=lat_lower, lat__lte=lat_upper, lng__gte=lng_lower, lng__lte=lng_upper)
            values = addresses.values('event_id')
            values_list = []
            for value in values:
                values_list.append(value['event_id'])

            # get base events
            events = super(EventResource, self).get_object_list(request)

            # the possible time GET params to filter on events
            possible_time_params = [
                'start_at', 'start_at__gt', 'start_at__gte', 'start_at__lt', 'start_at__lte',
                'end_at', 'end_at__gt', 'end_at__gte', 'end_at__lt', 'end_at__lte',
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
                    (Q(start_at__gt=now_datetime) & Q(start_at__lte=post_now_datetime)) | (Q(start_at__lte=now_datetime) & Q(end_at__gte=now_datetime)) | (Q(end_at__lt=now_datetime) & Q(end_at__gte=pre_now_datetime))
                )

            return events.filter(pk__in=values_list)
        else:
            return super(EventResource, self).get_object_list(request)
