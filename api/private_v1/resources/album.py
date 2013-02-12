import api.auth
import api.base_v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from event import EventResource
from photo import PhotoResource
from type import TypeResource

class AlbumResource(api.base_v1.resources.AlbumResource):

    event = fields.ForeignKey(EventResource, 'event')
    type = fields.ForeignKey(TypeResource, 'type')

    Meta = api.base_v1.resources.AlbumResource.Meta # set Meta to the public API Meta
    Meta.fields += [] # fields = ['short_name', 'name', 'description', 'creation_date']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = Authorization()
