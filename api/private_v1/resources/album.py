import api.auth
import api.base_v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from event import EventResource
from photo import PhotoResource

class AlbumResource(api.base_v1.resources.AlbumResource):

    event = fields.ForeignKey(EventResource, 'event')

    class Meta(api.base_v1.resources.AlbumResource.Meta): # set Meta to the public API Meta
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()
