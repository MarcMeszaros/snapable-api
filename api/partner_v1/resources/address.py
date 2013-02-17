import api.auth
import api.base_v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from event import EventResource

class AddressResource(api.base_v1.resources.AddressResource):

    event = fields.ForeignKey(EventResource, 'event')

    Meta = api.base_v1.resources.AddressResource.Meta # set Meta to the public API Meta
    Meta.fields += ['address', 'lat', 'lng']
    Meta.include_resource_uri = False
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.DatabaseAuthentication()
    Meta.authorization = api.auth.DatabaseAuthorization()
