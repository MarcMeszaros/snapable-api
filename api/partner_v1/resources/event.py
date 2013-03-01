import api.auth
import api.base_v1.resources
import pytz

from datetime import datetime, timedelta
from decimal import Decimal

from django.conf.urls.defaults import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.http import HttpResponse, Http404

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ALL
from tastypie.validation import Validation

from account import AccountResource

from data.models import Account
from data.models import Address
from data.models import Event
from data.models import Guest
from data.models import Photo
from data.models import User

from api.utils import EventSerializer

class EventValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        required = ['account', 'end', 'start', 'title', 'url']
        for key in required:
            try:
                bundle.data[key]
            except KeyError:
                errors[key] = 'Missing field'

        # make sure there's only one account
        acc_str = bundle.data['account']
        acc_parts = acc_str.strip('/').split('/')
        account = Account.objects.get(pk=acc_parts[-1])
        if account.event_set.count() > 1:
            errors['account'] = 'Only one event per account allowed with the partner API.'

        for key, value in bundle.data.items():
            # if the addresses field is set
            if key == 'locations':
                # check the outer item
                errors[key] = "Cannot create endpoints via the event. Use the 'location' endpoint."
                # check the inner item

        return errors

class EventResource(api.base_v1.resources.EventResource):

    # relations
    account = fields.ForeignKey(AccountResource, 'account', help_text='Account resource')
    locations = fields.ToManyField('api.partner_v1.resources.LocationResource', 'address_set', null=True, full=True) 

    # virtual fields
    photo_count = fields.IntegerField(attribute='photo_count', readonly=True, help_text='The number of photos for the event.')

    class Meta(api.base_v1.resources.EventResource.Meta):
        fields = api.base_v1.resources.EventResource.Meta.fields + ['photo_count']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = api.auth.DatabaseAuthentication()
        authorization = api.auth.DatabaseAuthorization()
        validation = EventValidation()
        serializer = EventSerializer(formats=['json', 'jpeg'])
        filtering = dict(api.base_v1.resources.EventResource.Meta.filtering, **{
            'enabled': ['exact'],
            'account': ['exact'],
            'start': ALL,
            'end': ALL,
            'title': ALL,
            'url': ALL,
            'q': ['exact'],
        })

    def obj_create(self, bundle, **kwargs):
        bundle = super(EventResource, self).obj_create(bundle, **kwargs)

        # create a new guest
        user = bundle.obj.account.users.all()[0]
        guest = Guest(event=bundle.obj, type_id=1, email=user.email, name=user.name)
        guest.save()

        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        
        orm_filters = super(EventResource, self).build_filters(filters)

        if 'q' in filters:
            qset = (
                (Q(title__icontains=filters['q']) | Q(url__icontains=filters['q']))
            )
        
            orm_filters.update({'q': qset})

        return orm_filters


    def apply_filters(self, request, applicable_filters):
        # some local variables
        custom_filters = []
        custom_virtual_filters = dict()

        # queryset filters
        if 'q' in applicable_filters:
            custom_filters.append(applicable_filters.pop('q'))

        # inital filtering
        semi_filtered = super(EventResource, self).apply_filters(request, applicable_filters)

        # do our queryset filtering
        for custom_filter in custom_filters:
            semi_filtered = semi_filtered.filter(custom_filter)
        
        return semi_filtered

    # override the response
    def create_response(self, request, bundle, response_class=HttpResponse, **response_kwargs):
        """
        Override the default create_response method.
        """
        if (request.META['REQUEST_METHOD'] == 'GET' and request.GET.has_key('size')):
            bundle.data['size'] = request.GET['size']

        return super(EventResource, self).create_response(request, bundle, response_class=response_class, **response_kwargs)