# python
from datetime import datetime, timedelta

# django/tastypie/libs
import django
import pytz
import stripe

from django.conf import settings
from django.conf.urls import url
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from monthdelta import MonthDelta
from tastypie import fields, http
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, ImmediateHttpResponse
from tastypie.resources import ALL, ModelResource
from tastypie.utils import dict_strip_unicode_keys
from tastypie.validation import Validation

# snapable
import api.auth

from account import AccountResource
from data.models import Account, AccountAddon, EventAddon, Package, Order, User
from user import UserResource

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

class OrderResource(ModelResource):

    account = fields.ForeignKey(AccountResource, 'account')
    user = fields.ForeignKey(UserResource, 'user', null=True)

    amount = fields.IntegerField(attribute='amount', readonly=True, help_text='The amount of the order.')

    class Meta:
        queryset = Order.objects.all()
        fields = ['amount_refunded', 'timestamp', 'charge_id', 'items', 'paid', 'coupon']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'patch']
        account_allowed_methods = ['post']
        always_return_data = True
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()
        validation = OrderValidation()
        filtering = {
            'timestamp': ALL,
        }

    def dehydrate(self, bundle):
        # small hack required to make the field return as json
        bundle.data['items'] = bundle.obj.items

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['price'] = bundle.obj.amount

        return bundle

    def hydrate(self, bundle):
        if 'total_price' in bundle.data:
            bundle.data['amount'] = bundle.data['total_price']

        if 'payment_gateway_invoice_id' in bundle.data:
            bundle.data['charge_id'] = bundle.data['payment_gateway_invoice_id']

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
        user_resource = UserResource()
        updated_user_bundle = user_resource.obj_create(user_bundle, **kwargs)

        # update the bundle with the user and account, then call the regular order code
        bundle.data['user'] = user_resource.get_resource_uri(updated_user_bundle.obj)
        bundle.data['account'] = account_resource.get_resource_uri(updated_user_bundle.obj.account_set.all()[0])

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

        # receipt items
        receipt_items = list()

        # get the package
        package = None
        if 'package' in bundle.obj.items:
            package = Package.objects.get(pk=bundle.obj.items['package'])
            item = {'name': 'Snapable Event Package ({0})'.format(package.name), 'amount': package.amount}
            receipt_items.append(item)

        # add discount
        if 'discount' in bundle.data and bundle.data['discount'] >= 0:
            discount = bundle.data['discount']
            # if there is a coupon code
            if 'coupon' in bundle.data:
                item = {'name': 'Discount (coupon: "{0}")'.format(bundle.data['coupon']), 'amount': -discount}
            # no coupon code, just add generic discount line
            else:
                item = {'name': 'Discount', 'amount': -discount}

            receipt_items.append(item)

        # calculate the total
        total = 0
        for item in receipt_items:
            total += item['amount']

        # make sure the total is non-negative
        if total < 0:
            total = 0

        # set the actual total
        bundle.obj.amount = total
        bundle.obj.save()

        if 'stripeToken' in bundle.data and bundle.obj.amount >= 50:         
            user = bundle.obj.user
            # Create the charge on Stripe's servers - this will charge the user's card
            try:
                charge = None
                if user is not None:
                    # if there is no customer on stripe, create them
                    if user.stripe_customer_id is None:
                        customer = stripe.Customer.create(
                            card=bundle.data['stripeToken'],
                            email=user.email
                        )
                        # save the id for later
                        user.stripe_customer_id = customer.id
                        user.save()

                    # charge the card
                    charge = stripe.Charge.create(
                        amount=bundle.obj.amount, # in cents
                        currency=settings.STRIPE_CURRENCY,
                        customer=user.stripe_customer_id
                    )

                else:
                    charge = stripe.Charge.create(
                        amount=bundle.obj.amount, # amount in cents, again
                        currency=settings.STRIPE_CURRENCY,
                        card=bundle.data['stripeToken'],
                        description='Charge to {0}'.format(bundle.obj.user.email)
                    )
                bundle.obj.charge_id = charge.id
                bundle.obj.paid = True
                bundle.obj.save()
            except stripe.CardError, e:
                # The card has been declined
                print e
                raise ImmediateHttpResponse('Error processing Credit Card')

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

        ## send the receipt ##
        # load in the templates
        plaintext = get_template('receipt.txt')
        html = get_template('receipt.html')

        # setup the template context variables
        d = Context({
            'items': receipt_items,
            'total': total,
        })

        # build the email
        subject, from_email, to = 'Your Snapable order has been processed', 'support@snapable.com', [bundle.obj.user.email]
        text_content = plaintext.render(d)
        html_content = html.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        if settings.DEBUG == False:
            msg.send()

        return bundle