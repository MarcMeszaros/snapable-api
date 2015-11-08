# django/tastypie/libs
from tastypie import fields
from tastypie.resources import ALL

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import AccountUser

class AccountUserResource(BaseModelResource):

    account = fields.ForeignKey('api.private_v1.resources.AccountResource', 'account')
    user = fields.ForeignKey('api.private_v1.resources.UserResource', 'user')

    class Meta(BaseMeta):
        queryset = AccountUser.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        filtering = {
            'account': ALL,
            'user': ALL,
        }