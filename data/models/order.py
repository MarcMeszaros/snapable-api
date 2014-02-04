# django/tastypie/libs
from django.db import models
from django.contrib import admin
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField

# snapable
from data.models import Account
from data.models import User

@python_2_unicode_compatible
class Order(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    account = models.ForeignKey(Account)
    user = models.ForeignKey(User, null=True)

    amount = models.IntegerField(default=0, help_text='The order amount. (USD cents)')
    amount_refunded = models.IntegerField(default=0, help_text='The amount refunded. (USD cents)')
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the order was processed. (UTC)')
    items = JSONField(help_text='The items payed for.')
    charge_id = models.CharField(max_length=255, null=True, help_text='The invoice id for the payment gateway.')
    paid = models.BooleanField(default=False, help_text='If the order has been paid for.')
    coupon = models.CharField(max_length=255, null=True, default=None, help_text='The coupon code used in the order.')

    ## virtual properties getters/setters ##
    # return the created at timestamp
    def _get_timestamp(self):
        return self.created_at

    def _set_timestamp(self, value):
        self.created_at = value

    # add the virtual properties
    timestamp = property(_get_timestamp, _set_timestamp)

    def __str__(self):
        return '{0} - ${1:.2f}(-${2:.2f}) [{3}] {4}'.format(self.pk, (self.amount/100.0), (self.amount_refunded/100.0), self.coupon, self.charge_id)

    def __repr__(self):
        return str({
            'amount': self.amount,
            'amount_refunded': self.amount_refunded,
            'charge_id': self.charge_id,
            'coupon': self.coupon,
            'created_at': self.created_at,
            'paid': self.paid,
        })

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)
