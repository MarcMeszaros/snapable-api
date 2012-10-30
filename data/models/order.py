from django.db import models
from jsonfield import JSONField

from data.models import Account

class Order(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    account = models.ForeignKey(Account)

    total_price = models.DecimalField(max_digits=6, decimal_places=2, help_text='The per unit addon price.') # 9999.99
    timestamp = models.DateTimeField(auto_now_add=True, help_text='When the order was processed. (UTC)')
    items = JSONField(help_text='The items payed for.')
    shipping = JSONField(null=True, help_text='Shipping information.')
    payment_gateway_invoice_id = models.CharField(max_length=255, null=True, help_text='The invoice id for the payment gateway.')
    print_gateway_invoice_id = models.CharField(max_length=255, null=True, help_text='The invoice id for the print gateway.')
    paid = models.BooleanField(default=False, help_text='If the order has been paid for.')