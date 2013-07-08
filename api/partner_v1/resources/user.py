# django/tastypie/libs
from tastypie import fields

# snapable
import api.auth
import api.base_v1.resources

from data.models import Account, AccountUser, User

class UserResource(api.base_v1.resources.UserResource):

    # the accounts the user belongs to
    #accounts = fields.ToManyField('api.partner_v1.resources.AccountResource', 'account_set', default=None, blank=True, null=True)

    class Meta(api.base_v1.resources.UserResource.Meta):
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'patch']
        authentication = api.auth.DatabaseAuthentication()
        authorization = api.auth.DatabaseAuthorization()

    def dehydrate(self, bundle):
        apikey = api.auth.DatabaseAuthentication().get_identifier(bundle.request)
        # get the accounts the user belongs to
        json_accounts = []
        for account in bundle.obj.account_set.filter(api_account=apikey.account):
            json_accounts.append('/partner_v1/account/{0}/'.format(account.pk))

        bundle.data['accounts'] = json_accounts

        return bundle

    def obj_create(self, bundle, **kwargs):
        # get the API key associated with the request
        apikey = api.auth.DatabaseAuthentication().get_identifier(bundle.request)

        # try and get an existing user
        try:
            bundle.obj = User.objects.get(email=bundle.data['email'])
        # no existing user, create them
        except User.DoesNotExist as e:
            if 'password' not in bundle.data:
                kwargs['password'] = User.generate_password(api.auth.get_nonce(32))

            bundle = super(UserResource, self).obj_create(bundle, **kwargs)

        # create a new account entry
        account = Account()
        account.api_account = apikey.account # set the api key's account as the creator
        account.save()

        # add the user as an admin to the new account
        accountuser = AccountUser(account=account, user=bundle.obj, admin=True)
        accountuser.save()

        return bundle