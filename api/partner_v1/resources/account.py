# django/tastypie/libs
from tastypie import fields

# snapable
import api.auth
import api.base_v1.resources

from data.models import Account, User
from user import UserResource

class AccountResource(api.base_v1.resources.AccountResource):

    users = fields.ManyToManyField('api.partner_v1.resources.UserResource', 'users', full=True)

    class Meta(api.base_v1.resources.AccountResource.Meta):
        fields = ['resource_uri']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authentication = api.auth.DatabaseAuthentication()
        authorization = api.auth.DatabaseAuthorization()