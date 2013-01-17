import api.auth

from tastypie import fields
from tastypie.resources import ModelResource
from data.models import Order

from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest

from account import AccountResource
from user import UserResource

from data.models import AccountAddon
from data.models import EventAddon
from data.models import Package

class OrderResource(ModelResource):

    account = fields.ForeignKey(AccountResource, 'account')
    user = fields.ForeignKey(UserResource, 'user', null=True)

    class Meta:
        queryset = Order.objects.all()
        fields = ['total_price', 'timestamp', 'payment_gateway_invoice_id', 'print_gateway_invoice_id', 'items', 'shipping', 'paid', 'coupon']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()

    def dehydrate(self, bundle):
        # small hack required to make the field return as json
        bundle.data['items'] = bundle.obj.items
        bundle.data['shipping'] = bundle.obj.shipping

        return bundle


    def hydrate(self, bundle):
        # check the items data if it's set
        if bundle.data.has_key('items'):
            # get a handle on the items
            items = bundle.data['items']

            # make sure it is a JSONObject
            if type(items) is not dict:
                raise BadRequest('Must be a JSONObject.')

            # make sure the 3 different fields aren't missing
            if not items.has_key('package'):
                raise BadRequest('Missing "package" identifier.')
            if not items.has_key('account_addons') or type(items['account_addons']) is not list:
                raise BadRequest('Missing/improperly formated "account_addons" list.')
            if not items.has_key('event_addons') or type(items['event_addons']) is not list:
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

        # check the shipping data if it's set
        if bundle.data.has_key('shipping'):
            # get a handle on the shipping details
            shipping = bundle.data['shipping']

            # make sure it is a JSONObject
            if type(shipping) is not dict:
                raise BadRequest('Must be a JSONObject.')

            # make sure the different fields aren't missing
            if not shipping.has_key('name'):
                raise BadRequest('Missing "name" parameter.')
            if not shipping.has_key('street_address'):
                raise BadRequest('Missing "street_address" parameter.')
            if not shipping.has_key('city'):
                raise BadRequest('Missing "city" parameter.')
            if not shipping.has_key('state'):
                raise BadRequest('Missing "state" parameter.')
            if not shipping.has_key('country'):
                raise BadRequest('Missing "country" parameter.')
            if not shipping.has_key('zip'):
                raise BadRequest('Missing "zip" parameter.')

        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(OrderResource, self).obj_create(bundle, request)

        # loop through account_addons & event_addons and mark as paid
        # mark all the account addons as paid for
        for account_addon in bundle.obj.items['account_addons']:
            addon = AccountAddon.objects.get(pk=account_addon)
            addon.paid = True
            addon.save()

        # mark all the event addons as paid for
        for event_addon in bundle.obj.items['event_addons']:
            addon = EventAddon.objects.get(pk=event_addon)
            addon.paid = True
            addon.save()

        return bundle