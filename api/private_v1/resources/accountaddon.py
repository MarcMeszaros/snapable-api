from tastypie import fields
from tastypie.resources import ALL, ModelResource
from data.models import AccountAddon

from addon import AddonResource
from event import EventResource

class AccountAddonResource(ModelResource):

    event = fields.ForeignKey(EventResource, 'event')
    addon = fields.ForeignKey(AddonResource, 'addon')

    class Meta:
        queryset = AccountAddon.objects.all()
        fields = ['quantity', 'paid']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        filtering = {
            'event': ALL,
            'addon': ALL,
        }