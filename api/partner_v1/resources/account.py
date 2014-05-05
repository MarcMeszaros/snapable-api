# django/tastypie/libs
from tastypie import fields

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Account

class AccountResource(BaseModelResource):

    users = fields.ManyToManyField('api.partner_v1.resources.UserResource', 'users')

    class Meta(BaseMeta):
        queryset = Account.objects.all()
        fields = ['resource_uri']