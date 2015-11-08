# django/tastypie/libs
from tastypie import fields

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Account

class AccountResource(BaseModelResource):

    package = fields.ForeignKey('api.private_v1.resources.PackageResource', 'package', null=True)
    addons = fields.ManyToManyField('api.private_v1.resources.AccountAddonResource', 'accountaddon_set', null=True, full=True)
    users = fields.ManyToManyField('api.private_v1.resources.AccountUserResource', 'accountuser_set', full=True)

    class Meta(BaseMeta): # set Meta to the public API Meta
        queryset = Account.objects.all()
        fields = ['valid_until']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'put', 'patch']
