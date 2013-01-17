from django.db import models
from jsonfield import JSONField

from data.models import Account
from data.models import User

class Order(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    account = models.ForeignKey(Account)
    user = models.ForeignKey(User, null=True)

    total_price = models.IntegerField(help_text='The per unit addon price. (CENTS)')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='When the order was processed. (UTC)')
    items = JSONField(help_text='The items payed for.')
    shipping = JSONField(null=True, help_text='Shipping information.')
    payment_gateway_invoice_id = models.CharField(max_length=255, null=True, help_text='The invoice id for the payment gateway.')
    print_gateway_invoice_id = models.CharField(max_length=255, null=True, help_text='The invoice id for the print gateway.')
    paid = models.BooleanField(default=False, help_text='If the order has been paid for.')
    coupon = models.CharField(max_length=255, null=True, default=None, help_text='The coupon code used in the order.')