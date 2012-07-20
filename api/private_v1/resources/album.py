import api.v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from event import EventResource

class AlbumResource(api.v1.resources.AlbumResource):

    event = fields.ForeignKey(EventResource, 'event')

    Meta = api.v1.resources.AlbumResource.Meta # set Meta to the public API Meta
    Meta.list_allowed_methods += ['post']
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.AlbumResource.__init__(self)