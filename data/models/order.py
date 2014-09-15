# -*- coding: utf-8 -*-
# python
import re

# django/libs
import stripe
from django.contrib import admin
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

# snapable
import dashboard
import utils.currency
import utils.sendwithus
from accountaddon import AccountAddon
from eventaddon import EventAddon
from package import Package


@python_2_unicode_compatible
class Order(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    # the choices for the interval field
    # name should contain the [value] in cents
    COUPON_CHOICES = [
        ('201bride', '201bride -¢[1000]'),  # added 2013-03-26
        ('adorii', 'adorii -¢[4900]'),  # added 2013-01-24
        ('adorii5986', 'adorii5986 -¢[4900]'),  # added 2013-02-06
        ('bespoke', 'bespoke -¢[1000]'),  # added 2013-01-31
        ('betheman', 'betheman -¢[1000]'),  # added 2013-01-31
        ('bridaldetective', 'bridaldetective -¢[1000]'),  # added 2013-01-31
        ('budgetsavvy', 'budgetsavvy -¢[1000]'),  # added 2013-02-26
        ('enfianced', 'enfianced -¢[1000]'),  # added 2013-01-31
        ('gbg', 'gbg -¢[1000]'),  # added 2013-01-31
        ('nonprofitedu', 'nonprofitedu -¢[4900]'),  # added 2014-02-20
        ('poptastic', 'poptastic -¢[1000]'),  # added 2013-01-31
        ('smartbride', 'smartbride -¢[1000]'),  # added 2013-01-31
        ('snaptrial2013', 'snaptrial2013 -¢[4900]'),  # added 2013-03-14
        ('snaptrial2014', 'snaptrial2014 -¢[4900]'),  # added 2014-02-20
        ('weddingful5986', 'weddingful5986 -¢[4900]'),  # added 2013-02-06
        ('wr2013', 'wr2013 -¢[1000]'),  # added 2013-01-17
    ]

    account = models.ForeignKey('Account', help_text='The account that the order is for.')
    user = models.ForeignKey('User', null=True, help_text='The user that made the order.')

    amount = models.IntegerField(default=0, help_text='The order amount. (USD cents)')
    amount_refunded = models.IntegerField(default=0, help_text='The amount refunded. (USD cents)')
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the order was processed. (UTC)')
    items = JSONField(help_text='The items payed for.')
    charge_id = models.CharField(max_length=255, null=True, help_text='The invoice id for the payment gateway.')
    is_paid = models.BooleanField(default=False, help_text='If the order has been paid for.')
    coupon = models.CharField(max_length=255, null=True, default=None, choices=COUPON_CHOICES, help_text='The coupon code used in the order.')

    def __str__(self):
        return u'{0} - ${1:.2f} {2} ({3})'.format(self.pk, (self.amount - self.amount_refunded)/100.0, self.charge_id, self.coupon)

    def __repr__(self):
        return str({
            'amount': self.amount,
            'amount_refunded': self.amount_refunded,
            'charge_id': self.charge_id,
            'coupon': self.coupon,
            'created_at': self.created_at,
            'is_paid': self.is_paid,
        })

    def get_coupon_discount(self):
        try:
            dictionary = dict(self.COUPON_CHOICES)
            return abs(int(re.search('\[(\d+)\]$', dictionary[self.coupon]).group(1)))
        except KeyError:
            return 0

    def calculate(self, discount=0):
        total = 0

        if 'package' in self.items:
            package = Package.objects.get(pk=self.items['package'])
            total += package.amount

        # loop through account_addons & event_addons and mark as paid
        # mark all the account addons as paid for
        if 'account_addons' in self.items:
            for account_addon in self.items['account_addons']:
                addon = AccountAddon.objects.get(pk=account_addon)
                total += addon.amount

        # mark all the event addons as paid for
        if 'event_addons' in self.items:
            for event_addon in self.items['event_addons']:
                addon = EventAddon.objects.get(pk=event_addon)
                total += addon.amount

        if discount <= 0 and self.coupon:
            discount = self.get_coupon_discount()

        # update the amount
        #if not self.is_paid:
        self.amount = total - discount


    def charge(self, stripe_token=None):
        if self.is_paid or self.amount < 50:
            return False

        try:
            charge = None
            if self.user is not None:
                # if there is no customer on stripe, create them
                if self.user.stripe_customer_id is None:
                    customer = stripe.Customer.create(
                        card=stripe_token,
                        email=self.user.email
                    )
                    # save the id for later
                    self.user.stripe_customer_id = customer.id
                    self.user.save()

                # charge the card
                charge = stripe.Charge.create(
                    amount=self.amount,  # in cents
                    currency=settings.STRIPE_CURRENCY,
                    customer=self.user.stripe_customer_id
                )
            else:
                charge = stripe.Charge.create(
                    amount=self.amount,  # amount in cents, again
                    currency=settings.STRIPE_CURRENCY,
                    card=stripe_token,
                    description='Charge to {0}'.format(self.user.email)
                )
            self.charge_id = charge.id
            self.is_paid = True
            self.save()

            # loop through account_addons & event_addons and mark as paid
            # mark all the account addons as paid for
            if 'account_addons' in self.items:
                for account_addon in self.items['account_addons']:
                    addon = AccountAddon.objects.get(pk=account_addon)
                    addon.is_paid = True
                    addon.save()

            # mark all the event addons as paid for
            if 'event_addons' in self.items:
                for event_addon in self.items['event_addons']:
                    addon = EventAddon.objects.get(pk=event_addon)
                    addon.is_paid = True
                    addon.save()

            return True
        except:
            return False

    def send_email(self):
        receipt_items = list()

        # add the package
        if 'package' in self.items:
            package = Package.objects.get(pk=self.items['package'])
            description = 'Snapable Event Package ({0})'.format(package.name)
            amount_str = utils.currency.cents_to_str(package.amount)
            item = {'name': description, 'description': description, 'amount': amount_str}
            receipt_items.append(item)

        # add the coupons
        if self.coupon:
            description = 'Discount (coupon: {0})'.format(self.coupon)
            amount_str = utils.currency.cents_to_str(-self.get_coupon_discount())
            discount = {'name': description, 'description': description, 'amount': amount_str}
            receipt_items.append(discount)

        ## send the receipt ##
        # sendwithus
        email_data = {
            'order': {
                'total': utils.currency.cents_to_str(self.amount),
                'lines': receipt_items,
                'created_at': self.created_at,
            }
        }

        r = utils.sendwithus.api.send(
            email_id='8mVTzXEJEvfXXCrwJFegHa',
            recipient={'address': self.user.email},
            email_data=email_data
        )


#===== Admin =====#
# base details for direct and inline admin models
class OrderAdminDetails(object):
    list_display = ['id', 'amount', 'amount_refunded', 'is_paid', 'coupon', 'created_at']
    list_filter = ['is_paid', 'created_at']
    readonly_fields = ['id', 'charge_id', 'account', 'user']
    search_fields = ['coupon']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                ('charge_id', 'coupon'),
                ('amount', 'amount_refunded'),
                'items',
                'is_paid',
            ),
        }),
        ('Ownership', {
            'classes': ('collapse',),
            'fields': (
                'account',
                'user',
            )
        }),
    )


# add the direct admin model
@admin.register(Order, site=dashboard.site)
class OrderAdmin(admin.ModelAdmin, OrderAdminDetails):
    actions = ['charge', 'send_email']

    def send_email(self, request, queryset):
        for order in queryset.iterator():
            order.send_email()

        self.message_user(request, 'Successfully sent receipt emails.')

    def charge(self, request, queryset):
        success = True
        for order in queryset.iterator():
            success = success and order.charge()

        if success:
            self.message_user(request, 'Sent charge requests')
        else:
            self.message_user(request, 'Some charges failed')


# add the inline admin model
class OrderAdminInline(admin.StackedInline, OrderAdminDetails):
    model = Order

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
