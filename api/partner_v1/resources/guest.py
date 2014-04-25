# django/tastypie/libs
from tastypie import fields
from tastypie.resources import ALL

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Guest

class GuestResource(BaseModelResource):

    event = fields.ForeignKey('api.partner_v1.resources.EventResource', 'event')

    class Meta(BaseMeta): # set Meta to the public API Meta
        queryset = Guest.objects.all()
        fields = ['name', 'email']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        filtering = {
            'event': ['exact'],
            'email': ALL,
        }