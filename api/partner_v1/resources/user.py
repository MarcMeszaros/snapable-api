import api.auth
import api.base_v1.resources

from tastypie import fields

from data.models import Account
from data.models import AccountUser
from data.models import User

class UserResource(api.base_v1.resources.UserResource):

    # the accounts the user belongs to
    accounts = fields.ToManyField('api.partner_v1.resources.AccountResource', 'account_set', default=None, blank=True, null=True)

    class Meta(api.base_v1.resources.UserResource.Meta):
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put']
        authentication = api.auth.DatabaseAuthentication()
        authorization = api.auth.DatabaseAuthorization()

    def obj_create(self, bundle, **kwargs):
        bundle = super(UserResource, self).obj_create(bundle, **kwargs)

        # create a new account entry and set the new user as the admin
        account = Account()
        account.save()

        # add the user as an admin to the new account
        accountuser = AccountUser(account=account, user=bundle.obj, admin=True)
        accountuser.save()

        return bundle