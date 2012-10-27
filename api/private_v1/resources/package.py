import api.auth
import api.v1.resources
from tastypie.authorization import Authorization
from tastypie.resources import ALL

class PackageResource(api.v1.resources.PackageResource):

    Meta = api.v1.resources.PackageResource.Meta # set Meta to the public API Meta
    Meta.fields += []
    Meta.list_allowed_methods = ['get']
    Meta.detail_allowed_methods = ['get']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = Authorization()
    Meta.filtering = {
        'short_name': ALL,
    }

    def __init__(self):
        api.v1.resources.PackageResource.__init__(self)
