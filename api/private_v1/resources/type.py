import api.auth
import api.base_v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

class TypeResource(api.base_v1.resources.TypeResource):

    Meta = api.base_v1.resources.TypeResource.Meta # set Meta to the public API Meta
    Meta.fields += ['name']
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = Authorization()