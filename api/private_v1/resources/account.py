import api.auth
import api.v1.resources
from tastypie import fields

from data.models import Account
from data.models import User

from user import UserResource

class AccountResource(api.v1.resources.AccountResource):

    admin = fields.ForeignKey(UserResource, 'admin')

    Meta = api.v1.resources.AccountResource.Meta # set Meta to the public API Meta
    Meta.fields += ['admin']
    Meta.list_allowed_methods = ['get']
    Meta.detail_allowed_methods = ['get']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = api.auth.ServerAuthorization()
