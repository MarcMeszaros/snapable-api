import api.v1.resources
from tastypie.authorization import Authorization

class PhotoResource(api.v1.resources.PhotoResource):

    Meta = api.v1.resources.PhotoResource.Meta # set Meta to the public API Meta
    Meta.list_allowed_methods += ['post']
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.PhotoResource.__init__(self)