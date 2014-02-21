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
from accountaddon import AccountAddon
from eventaddon import EventAddon
from package import Package
from utils.loggers import Log

@python_2_unicode_compatible
class Order(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    account = models.ForeignKey('Account', help_text='The account that the order is for.')
    user = models.ForeignKey('User', null=True, help_text='The user that made the order.')

    amount = models.IntegerField(default=0, help_text='The order amount. (USD cents)')
    amount_refunded = models.IntegerField(default=0, help_text='The amount refunded. (USD cents)')
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the order was processed. (UTC)')
    items = JSONField(help_text='The items payed for.')
    charge_id = models.CharField(max_length=255, null=True, help_text='The invoice id for the payment gateway.')
    is_paid = models.BooleanField(default=False, help_text='If the order has been paid for.')
    coupon = models.CharField(max_length=255, null=True, default=None, help_text='The coupon code used in the order.')

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


    def send_email_with_discount(self, discount=None):
        # receipt items
        receipt_items = list()

        if 'package' in self.items:
            package = Package.objects.get(pk=self.items['package'])
            item = {'name': 'Snapable Event Package ({0})'.format(package.name), 'amount': package.amount}
            receipt_items.append(item)

        # add discounts
        if type(discount) == list and len(discount) > 0:
            for item in discount:
                receipt_items.append(item)

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

#===== Admin =====#
# base details for direct and inline admin models
class OrderAdminDetails(object):
    list_display = ['id', 'amount', 'amount_refunded', 'is_paid', 'coupon', 'created_at']
    list_filter = ['is_paid', 'created_at']
    readonly_fields = ['id', 'charge_id', 'coupon', 'account', 'user']
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
    pass
admin.site.register(Order, OrderAdmin)

# add the inline admin model
class OrderAdminInline(OrderAdminDetails, admin.StackedInline):
    model = Order

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
