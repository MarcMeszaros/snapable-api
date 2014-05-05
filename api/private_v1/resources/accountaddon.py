# django/tastypie/libs
from tastypie import fields
from tastypie.resources import ALL

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import AccountAddon

class AccountAddonResource(BaseModelResource):

    account = fields.ForeignKey('api.private_v1.resources.AccountResource', 'account')
    addon = fields.ForeignKey('api.private_v1.resources.AddonResource', 'addon', full=True)

    class Meta(BaseMeta):
        queryset = AccountAddon.objects.all()
        fields = ['quantity', 'paid']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        filtering = {
            'account': ALL,
            'addon': ALL,
        }