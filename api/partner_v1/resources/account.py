import api.auth
import api.base_v1.resources

from tastypie import fields

from data.models import Account
from data.models import User

from user import UserResource

class AccountResource(api.base_v1.resources.AccountResource):

    users = fields.ManyToManyField('api.partner_v1.resources.UserResource', 'users', full=True)

    class Meta(api.base_v1.resources.AccountResource.Meta):
        fields = ['resource_uri']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = api.auth.DatabaseAuthentication()
        authorization = api.auth.DatabaseAuthorization()