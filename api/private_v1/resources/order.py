from tastypie import fields
from tastypie.resources import ModelResource
from data.models import Order

from event import EventResource

class OrderResource(ModelResource):

    event = fields.ForeignKey(EventResource, 'event')

    class Meta:
        queryset = Order.objects.all()
        fields = ['total', 'timestamp', 'payment_gateway_invoice_id', 'print_gateway_invoice_id', 'items']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put']
        always_return_data = True