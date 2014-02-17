# django/tastypie/libs
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.template.loader import get_template
from django.template import Context
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

# snapable
import admin
from package import Package

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
    paid = models.BooleanField(default=False, help_text='If the order has been paid for.')
    coupon = models.CharField(max_length=255, null=True, default=None, help_text='The coupon code used in the order.')

    def __str__(self):
        return u'{0} - ${1:.2f} {2} ({3})'.format(self.pk, (self.amount - self.amount_refunded)/100.0, self.charge_id, self.coupon)

    def __repr__(self):
        return str({
            'amount': self.amount,
            'amount_refunded': self.amount_refunded,
            'charge_id': self.charge_id,
            'coupon': self.coupon,
            'created_at': self.created_at,
            'paid': self.paid,
        })

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
        if settings.DEBUG == False:
            msg.send()

#===== Admin =====#
# base details for direct and inline admin models
class OrderAdminDetails(object):
    list_display = ['id', 'amount', 'amount_refunded', 'paid', 'coupon', 'created_at']
    list_filter = ['paid', 'created_at']
    readonly_fields = ['id', 'charge_id', 'coupon', 'account', 'user']
    search_fields = ['coupon']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                ('charge_id', 'coupon'), 
                ('amount', 'amount_refunded'),
                'items',
                'paid',
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
