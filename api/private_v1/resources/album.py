import api.v1.resources
from tastypie.authorization import Authorization

class AlbumResource(api.v1.resources.AlbumResource):

    Meta = api.v1.resources.UserResource.Meta # set Meta to the public API Meta
    Meta.list_allowed_methods += ['post']
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.AlbumResource.__init__(self)