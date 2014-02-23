# django/libs
import stripe
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

# snapable
import admin
#import utils.sendwithus
from accountaddon import AccountAddon
from eventaddon import EventAddon
from package import Package
from utils.loggers import Log

@python_2_unicode_compatible
class Order(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    # the choices for the interval field
    COUPON_CHOICES = (
        ('201bride', '201bride (-$10)'), # 1000, // added: 2013-03-26; valid_until: TBD
        ('adorii', 'adorii (-$49)'), # 4900, // added: 2013-01-24; valid_until: TBD
        ('adorii5986', 'adorii5986 (-$49)'), # 4900, // added: 2013-02-06; valid_until: TBD
        ('bespoke', 'bespoke (-$10)'), # 1000, // added: 2013-01-31; valid_until: TBD
        ('betheman', 'betheman (-$10)'), # 1000, // added: 2013-01-31; valid_until: TBD
        ('bridaldetective', 'bridaldetective (-$10)'), # 1000, // added: 2013-01-31; valid_until: TBD
        ('budgetsavvy', 'budgetsavvy (-$10)'), # 1000, // added: 2013-02-26; valid_until: TBD
        ('enfianced', 'enfianced (-$10)'),# 1000, // added: 2013-01-31; valid_until: TBD
        ('gbg', 'gbg (-$10)'), # 1000, // added: 2013-01-31; valid_until: TBD
        ('nonprofitedu', 'nonprofitedu (-$49)'), # 4900, // added: 2014-02-20; valid_until: TBD
        ('poptastic', 'poptastic (-$10)'), # 1000, // added: 2013-01-31; valid_until: TBD
        ('smartbride', 'smartbride (-$10)'), # 1000, // added: 2013-01-31; valid_until: TBD
        ('snaptrial2013', 'snaptrial2013 (-$49)'), # 4900, // added: 2013-03-14; valid_until: TBD
        ('snaptrial2014', 'snaptrial2014 (-$49)'), # 4900, // added: 2014-02-20; valid_until: TBD
        ('weddingful5986', 'weddingful5986 (-$49)'), # 4900, // added: 2013-02-06; valid_until: TBD
        ('wr2013', 'wr2013 (-$10)'), # 1000, // added: 2013-01-17; valid_until: TBD
    )
    COUPON_PRICES = {
        '201bride': 1000,
        'adorii': 4900,
        'adorii5986': 4900,
        'bespoke': 1000,
        'betheman': 1000,
        'bridaldetective': 1000,
        'budgetsavvy': 1000,
        'enfianced': 1000,
        'gbg': 1000,
        'nonprofitedu': 4900,
        'poptastic': 1000,
        'smartbride': 1000,
        'snaptrial2013': 4900,
        'snaptrial2014': 4900,
        'weddingful5986': 4900,
        'wr2013': 1000,
    }

    account = models.ForeignKey('Account', help_text='The account that the order is for.')
    user = models.ForeignKey('User', null=True, help_text='The user that made the order.')

    amount = models.IntegerField(default=0, help_text='The order amount. (USD cents)')
    amount_refunded = models.IntegerField(default=0, help_text='The amount refunded. (USD cents)')
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the order was processed. (UTC)')
    items = JSONField(help_text='The items payed for.')
    charge_id = models.CharField(max_length=255, null=True, help_text='The invoice id for the payment gateway.')
    is_paid = models.BooleanField(default=False, help_text='If the order has been paid for.')
    coupon = models.CharField(max_length=255, null=True, default=None, choices=COUPON_CHOICES, help_text='The coupon code used in the order.')

    @property
    def paid(self):
        Log.deprecated('Order.paid is deprecated, use Order.is_paid')
        return self.is_paid

    @paid.setter
    def paid(self, value):
        Log.deprecated('Order.paid is deprecated, use Order.is_paid')
        self.is_paid = value

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

        # update the amount
        #if not self.paid:
        self.amount = total - discount


    def charge(self, stripe_token):
        if self.paid or self.amount < 50:
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
                    amount=self.amount, # in cents
                    currency=settings.STRIPE_CURRENCY,
                    customer=self.user.stripe_customer_id
                )

            else:
                charge = stripe.Charge.create(
                    amount=self.amount, # amount in cents, again
                    currency=settings.STRIPE_CURRENCY,
                    card=stripe_token,
                    description='Charge to {0}'.format(self.user.email)
                )
            self.charge_id = charge.id
            self.paid = True
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
            #raise ImmediateHttpResponse('Error processing Credit Card')

    def send_email(self):
        receipt_items = list()

        # add the package
        if 'package' in self.items:
            package = Package.objects.get(pk=self.items['package'])
            description = 'Snapable Event Package ({0})'.format(package.name)
            item = {'name': description, 'description': description, 'amount': package.amount}
            receipt_items.append(item)

        # add the coupons
        if self.coupon in self.COUPON_PRICES:
            description = 'Discount (coupon: {0})'.format(self.coupon)
            discount = {'name': description, 'description': description, 'amount': -self.COUPON_PRICES[self.coupon]}
            receipt_items.append(discount)

        ## send the receipt ##
        # load in the templates
        plaintext = get_template('receipt.txt')
        html = get_template('receipt.html')

        # setup the template context variables
        d = Context({
            'items': receipt_items,
            'total': self.amount,
        })

        # build the email
        subject, from_email, to = 'Your Snapable order has been processed', 'support@snapable.com', [self.user.email]
        text_content = plaintext.render(d)
        html_content = html.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # sendwithus
        #email_data = {
        #    'order': {
        #        'total': self.amount,
        #        'lines': receipt_items,
        #        #'created_at': self.created_at,
        #    }
        #}

        #r = utils.sendwithus.api.send(
        #    email_id='8mVTzXEJEvfXXCrwJFegHa',
        #    recipient={'address': self.user.email},
        #    email_data=email_data
        #)
        #Log.i('email send status: {0}'.format(r.status_code))

    def send_email_with_discount(self, discount=None):
        Log.deprecated('Order.send_email_with_discount() is deprecated, use Order.send_email() instead')
        self.send_email()

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
class OrderAdmin(OrderAdminDetails, admin.ModelAdmin):
    actions = ['send_email']

    def send_email(self, request, queryset):
        for order in queryset.iterator():
            order.send_email()

        self.message_user(request, "Successfully sent receipt emails.")

admin.site.register(Order, OrderAdmin)

# add the inline admin model
class OrderAdminInline(OrderAdminDetails, admin.StackedInline):
    model = Order

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
