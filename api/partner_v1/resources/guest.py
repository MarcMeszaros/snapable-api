# django/tastypie/libs
from tastypie import fields
from tastypie.authorization import Authorization

# snapable
import api.auth
import api.base_v1.resources

from data.models import Type
from event import EventResource

class GuestResource(api.base_v1.resources.GuestResource):

    event = fields.ForeignKey(EventResource, 'event')

    class Meta(api.base_v1.resources.GuestResource.Meta): # set Meta to the public API Meta
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = api.auth.DatabaseAuthentication()
        authorization = api.auth.DatabaseAuthorization()

    def hydrate(self, bundle):
        type = Type.objects.get(pk=5) # get 'Guest' type
        bundle.obj.type = type # set the default type for the partner API

        return bundle