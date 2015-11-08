# django/tastypie/libs
from tastypie import fields

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Location

class AddressResource(BaseModelResource):

    event = fields.ForeignKey('api.private_v1.resources.EventResource', 'event')

    class Meta(BaseMeta): # set Meta to the public API Meta
        queryset = Location.objects.all()
        fields = ['address', 'lat', 'lng']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
