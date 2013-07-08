import api.auth
import api.base_v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from event import EventResource

class GuestResource(api.base_v1.resources.GuestResource):

    event = fields.ForeignKey(EventResource, 'event')

    class Meta(api.base_v1.resources.GuestResource.Meta): # set Meta to the public API Meta
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()

    def dehydrate(self, bundle):

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['type'] = '/private_v1/type/6/'

        return bundle
