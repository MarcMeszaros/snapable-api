import api.v1.resources
from tastypie.authorization import Authorization

class PackageResource(api.v1.resources.PackageResource):

    Meta = api.v1.resources.PackageResource.Meta # set Meta to the public API Meta
    Meta.fields += []
    Meta.list_allowed_methods += ['get', 'post']
    Meta.detail_allowed_methods += ['get', 'post']
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.PackageResource.__init__(self)
