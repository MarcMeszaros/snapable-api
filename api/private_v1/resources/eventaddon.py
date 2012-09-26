from tastypie import fields
from tastypie.resources import ALL, ModelResource
from data.models import EventAddon

from addon import AddonResource
from event import EventResource
from order import OrderResource

class EventAddonResource(ModelResource):

    event = fields.ForeignKey(EventResource, 'event')
    addon = fields.ForeignKey(AddonResource, 'addon')
    order = fields.ForeignKey(OrderResource, 'order', null=True)

    class Meta:
        queryset = EventAddon.objects.all()
        fields = ['quantity', 'paid']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        filtering = {
            'event': ALL,
            'addon': ALL,
            'order': ALL,
        }
