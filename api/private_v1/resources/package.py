import api.auth
import api.base_v1.resources
from tastypie.authorization import Authorization
from tastypie.resources import ALL

class PackageResource(api.base_v1.resources.PackageResource):

    class Meta(api.base_v1.resources.PackageResource.Meta): # set Meta to the public API Meta
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()
        filtering = {
            'short_name': ALL,
            'enabled': ['exact'],
        }

    def dehydrate(self, bundle):

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['price'] = bundle.obj.amount

        return bundle