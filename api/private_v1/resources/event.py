import api.auth
import api.v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from package import PackageResource
from user import UserResource

class EventResource(api.v1.resources.EventResource):

    user = fields.ForeignKey(UserResource, 'user')
    package = fields.ForeignKey(PackageResource, 'package')

    Meta = api.v1.resources.EventResource.Meta # set Meta to the public API Meta
    Meta.fields += []
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = Authorization()
    Meta.filtering = dict(Meta.filtering, **{
        'user': ['exact'],
    })

    def __init__(self):
        api.v1.resources.EventResource.__init__(self)
