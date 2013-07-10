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
        fields = ['amount', 'amount_refunded', 'timestamp', 'payment_gateway_invoice_id', 'items', 'paid', 'coupon']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'patch']
        always_return_data = True
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()

    def dehydrate(self, bundle):
        # small hack required to make the field return as json
        bundle.data['items'] = bundle.obj.items

        return bundle

    def hydrate(self, bundle):
        if 'total_price' in bundle.data:
            bundle.data['amount'] = bundle.data['total_price']

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

    def obj_create(self, bundle, **kwargs):
        bundle = super(OrderResource, self).obj_create(bundle, **kwargs)

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