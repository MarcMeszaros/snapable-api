import api.auth
import api.v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from event import EventResource

class AddressResource(api.v1.resources.AddressResource):

    event = fields.ForeignKey(EventResource, 'event')

    Meta = api.v1.resources.AddressResource.Meta # set Meta to the public API Meta
    Meta.fields += ['address', 'lat', 'lng']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.AddressResource.__init__(self)