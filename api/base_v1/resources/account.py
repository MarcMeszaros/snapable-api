from tastypie.resources import ModelResource
from data.models import Account

class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        fields = []
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True