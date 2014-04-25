# django/tastypie/libs
from tastypie import fields
from tastypie.resources import ALL

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import EventAddon

class EventAddonResource(BaseModelResource):

    event = fields.ForeignKey('api.private_v1.resources.EventResource', 'event')
    addon = fields.ForeignKey('api.private_v1.resources.AddonResource', 'addon', full=True)

    class Meta(BaseMeta):
        queryset = EventAddon.objects.all()
        fields = ['quantity', 'paid']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        always_return_data = True
        filtering = {
            'event': ALL,
            'addon': ALL,
        }
