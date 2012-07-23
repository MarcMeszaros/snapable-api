import api.v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from event import EventResource
from guest import GuestResource
from type import TypeResource

class PhotoResource(api.v1.resources.PhotoResource):

    event = fields.ForeignKey(EventResource, 'event')
    guest = fields.ForeignKey(GuestResource, 'guest')
    type = fields.ForeignKey(TypeResource, 'type')

    Meta = api.v1.resources.PhotoResource.Meta # set Meta to the public API Meta
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.PhotoResource.__init__(self)