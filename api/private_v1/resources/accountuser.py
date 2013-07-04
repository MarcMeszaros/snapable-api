from tastypie import fields
from tastypie.resources import ALL, ModelResource
from data.models import AccountUser

from account import AccountResource
from user import UserResource

class AccountUserResource(ModelResource):

    account = fields.ForeignKey(AccountResource, 'account')
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = AccountUser.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        always_return_data = True
        filtering = {
            'account': ALL,
            'user': ALL,
        }