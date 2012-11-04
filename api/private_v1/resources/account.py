import api.auth
import api.v1.resources
from tastypie import fields

from data.models import Account
from data.models import User

from package import PackageResource
from user import UserResource

class AccountResource(api.v1.resources.AccountResource):

    package = fields.ForeignKey(PackageResource, 'package')
    addons = fields.ManyToManyField('api.private_v1.resources.AccountAddonResource', 'accountaddon_set', null=True, full=True)
    users = fields.ManyToManyField('api.private_v1.resources.AccountUserResource', 'accountuser_set', full=True)

    Meta = api.v1.resources.AccountResource.Meta # set Meta to the public API Meta
    #Meta.fields += ['admin']
    Meta.list_allowed_methods = ['get']
    Meta.detail_allowed_methods = ['get']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = api.auth.ServerAuthorization()
