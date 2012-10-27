from tastypie import fields
from tastypie.resources import ALL, ModelResource
from data.models import AccountAddon

from addon import AddonResource
from event import EventResource
from order import OrderResource

class AccountAddonResource(ModelResource):

    event = fields.ForeignKey(EventResource, 'event')
    addon = fields.ForeignKey(AddonResource, 'addon')
    order = fields.ForeignKey(OrderResource, 'order', null=True)

    class Meta:
        queryset = AccountAddon.objects.all()
        fields = ['quantity', 'paid']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        filtering = {
            'event': ALL,
            'addon': ALL,
            'order': ALL,
        }