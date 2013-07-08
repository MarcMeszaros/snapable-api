# django/tastypie/libs
from tastypie import fields
from tastypie.authorization import Authorization

# snapable
import api.auth
import api.base_v1.resources

from event import EventResource

class GuestResource(api.base_v1.resources.GuestResource):

    event = fields.ForeignKey(EventResource, 'event')

    class Meta(api.base_v1.resources.GuestResource.Meta): # set Meta to the public API Meta
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        authentication = api.auth.DatabaseAuthentication()
        authorization = api.auth.DatabaseAuthorization()