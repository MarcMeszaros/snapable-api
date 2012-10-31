from tastypie import fields
from tastypie.resources import ALL, ModelResource
from data.models import AccountAddon

from account import AccountResource
from addon import AddonResource

class AccountAddonResource(ModelResource):

    account = fields.ForeignKey(AccountResource, 'account')
    addon = fields.ForeignKey(AddonResource, 'addon', full=True)

    class Meta:
        queryset = AccountAddon.objects.all()
        fields = ['quantity', 'paid']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        filtering = {
            'account': ALL,
            'addon': ALL,
        }