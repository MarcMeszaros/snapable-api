import api.auth
import api.base_v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from event import EventResource

class AddressResource(api.base_v1.resources.AddressResource):

    event = fields.ForeignKey(EventResource, 'event')

    class Meta(api.base_v1.resources.AddressResource.Meta): # set Meta to the public API Meta
        fields = api.base_v1.resources.AddressResource.Meta.fields + ['address', 'lat', 'lng']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()
