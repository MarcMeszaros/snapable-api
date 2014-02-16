# django/tastypie/libs
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

# snapable
import admin

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
