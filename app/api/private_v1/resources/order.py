# python
import logging
from datetime import datetime, timedelta

# django/tastypie/libs
import django
import pytz
from django.conf.urls import url
from monthdelta import MonthDelta
from tastypie import fields, http
from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie.resources import ALL
from tastypie.utils import dict_strip_unicode_keys
from tastypie.validation import Validation

# snapable
from .meta import BaseMeta, BaseModelResource
from .account import AccountResource
from .address import AddressResource
from .event import EventResource
from .user import UserResource
from data.models import Account, AccountAddon, Event, EventAddon, Package, Order, User

logger = logging.getLogger('snapable')

class OrderValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        required = ['account', 'user']
        for key in required:
            try:
                bundle.data[key]
            except KeyError:
                errors[key] = 'Missing field'

        return errors


class OrderResource(BaseModelResource):

    account = fields.ForeignKey('api.private_v1.resources.AccountResource', 'account')
    user = fields.ForeignKey('api.private_v1.resources.UserResource', 'user', null=True)

    amount = fields.IntegerField(attribute='amount', readonly=True, help_text='The amount of the order.')

    # DEPRECATED
    # old "paid" flag (2014-08-04)
    paid = fields.BooleanField(attribute='is_paid', default=False)

    class Meta(BaseMeta):
        queryset = Order.objects.all()
        fields = ['amount_refunded', 'created_at', 'charge_id', 'items', 'is_paid', 'coupon']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'patch']
        account_allowed_methods = ['post']
        validation = OrderValidation()
        filtering = {
            'created_at': ALL,
        }

    def dehydrate(self, bundle):
        # small hack required to make the field return as json
        bundle.data['items'] = bundle.obj.items

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['price'] = bundle.obj.amount

        return bundle

    def hydrate(self, bundle):
        # check the items data if it's set
        if 'items' in bundle.data:
            # get a handle on the items
            items = bundle.data['items']

            # make sure it is a JSONObject
            if type(items) is not dict:
                raise BadRequest('Must be a JSONObject.')

            # make sure the 3 different fields aren't missing
            if 'package' not in items:
                raise BadRequest('Missing "package" identifier.')
            if 'account_addons' not in items or type(items['account_addons']) is not list:
                raise BadRequest('Missing/improperly formated "account_addons" list.')
            if 'event_addons' not in items or type(items['event_addons']) is not list:
                raise BadRequest('Missing/improperly formated "event_addons" list.')

            # tweak the data/sanitize it
            bundle.data['items']['package'] = int(items['package'])

            # verify the data exists
            if type(items['package']) is int and not Package.objects.filter(pk=items['package']).exists():
                raise BadRequest('The entered package does not exist.')
            if type(items['account_addons']) is list and len(items['account_addons']) > 0 and not AccountAddon.objects.filter(pk__in=items['account_addons']).exists():
                raise BadRequest('One or more account addon identifiers does not exist.')
            if type(items['event_addons']) is list and len(items['event_addons']) > 0 and not EventAddon.objects.filter(pk__in=items['event_addons']).exists():
                raise BadRequest('One or more event addon identifiers does not exist.')

        return bundle

    def hydrate_stripeToken(self, bundle):
        bundle.data['stripeToken'] = bundle.data['stripeToken'].strip()
        return bundle

    def prepend_urls(self):
        """
        Using override_url
        """
        return [
            url(r'^(?P<resource_name>%s)/account/$' % self._meta.resource_name, self.wrap_view('dispatch_account'), name="api_dispatch_account"),
        ]

    def dispatch_account(self, request, **kwargs):
        """
        A view for handling the various HTTP methods (GET/POST/PUT/DELETE) on
        a single resource.

        Relies on ``Resource.dispatch`` for the heavy-lifting.
        """
        return self.dispatch('account', request, **kwargs)

    def post_account(self, request, **kwargs):
        """
        Creates a new resource/object with the provided data.

        Calls ``obj_create`` with the provided data and returns a response
        with the new resource's location.

        If a new resource is created, return ``HttpCreated`` (201 Created).
        If ``Meta.always_return_data = True``, there will be a populated body
        of serialized data.
        """
        ### start copied from tasytpie ###
        if django.VERSION >= (1, 4):
            body = request.body
        else:
            body = request.raw_post_data
        deserialized = self.deserialize(request, body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        ## start custom code ##
        user_bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        # create user and account
        account_resource = AccountResource()
        address_resource = AddressResource()
        event_resource = EventResource()
        user_resource = UserResource()
        updated_user_bundle = user_resource.obj_create(user_bundle, **kwargs)

        # update the bundle with the user and account, then call the regular order code
        bundle.data['user'] = user_resource.get_resource_uri(updated_user_bundle.obj)
        bundle.data['account'] = account_resource.get_resource_uri(updated_user_bundle.obj.account_set.all()[0])
        updated_user_bundle.data['account'] = bundle.data['account']

        try:
            # create the event
            updated_event_bundle = event_resource.obj_create(updated_user_bundle, **kwargs)
            bundle.data['event'] = event_resource.get_resource_uri(updated_event_bundle.obj)
            updated_event_bundle.data['event'] = bundle.data['event']

            # create the location
            updated_location_bundle = address_resource.obj_create(updated_event_bundle, **kwargs)
        except:
            pass

        ## end custom code ##
        updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)
        ### end copied from tasytpie ###

    def obj_create(self, bundle, **kwargs):
        bundle = super(OrderResource, self).obj_create(bundle, **kwargs)

        # get the package
        package = None
        if 'package' in bundle.obj.items:
            package = Package.objects.get(pk=bundle.obj.items['package'])

        # set the actual total
        bundle.obj.calculate()
        bundle.obj.save()

        if 'event' in bundle.data:
            event_resource = EventResource()
            event = event_resource.get_via_uri(bundle.data['event'], request=bundle.request)
            event.is_enabled = True
            event.save()

        # update the account
        if package is not None and package.interval is not None:
            # calculate the valid until date
            expire = None
            now = datetime.now(tz=pytz.UTC)
            trialdays = timedelta(package.trial_period_days)
            if package.interval == Package.INTERVAL_YEAR:
                expire = now + MonthDelta(12 * int(package.interval_count)) + trialdays
            elif package.interval == Package.INTERVAL_MONTH:
                expire = now + MonthDelta(int(package.interval_count)) + trialdays
            elif package.interval == Package.INTERVAL_WEEK:
                expire = now + timedelta(7 * int(package.interval_count)) + trialdays
            else:
                expire = now + trialdays

            # modify the account
            account = bundle.obj.account
            account.package = package
            account.valid_until = expire
            account.save()

        if 'stripeToken' in bundle.data:
            bundle.obj.charge(stripe_token=bundle.data['stripeToken'])

        ## send the receipt ##
        bundle.obj.send_email()

        return bundle
