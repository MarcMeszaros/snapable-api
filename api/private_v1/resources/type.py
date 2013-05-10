import api.auth
import api.base_v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

class TypeResource(api.base_v1.resources.TypeResource):

    class Meta(api.base_v1.resources.TypeResource.Meta): # set Meta to the public API Meta
        fields = api.base_v1.resources.TypeResource.Meta.fields + ['name']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()