from tastypie import fields
from tastypie.resources import ModelResource
from data.models import Order

from account import AccountResource

class OrderResource(ModelResource):

    account = fields.ForeignKey(AccountResource, 'account')

    class Meta:
        queryset = Order.objects.all()
        fields = ['total', 'timestamp', 'payment_gateway_invoice_id', 'print_gateway_invoice_id', 'items']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True