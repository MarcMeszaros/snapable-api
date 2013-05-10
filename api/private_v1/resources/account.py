import api.auth
import api.base_v1.resources
from tastypie import fields
from tastypie.authorization import Authorization

from data.models import Account
from data.models import User

from package import PackageResource
from user import UserResource

class AccountResource(api.base_v1.resources.AccountResource):

    package = fields.ForeignKey(PackageResource, 'package', null=True)
    addons = fields.ManyToManyField('api.private_v1.resources.AccountAddonResource', 'accountaddon_set', null=True, full=True)
    users = fields.ManyToManyField('api.private_v1.resources.AccountUserResource', 'accountuser_set', full=True)

    class Meta(api.base_v1.resources.AccountResource.Meta): # set Meta to the public API Meta
        fields = api.base_v1.resources.AccountResource.Meta.fields + ['valid_until']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'put']
        authentication = api.auth.ServerAuthentication()
        authorization = Authorization()
