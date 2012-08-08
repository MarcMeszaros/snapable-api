from tastypie.resources import ModelResource
from data.models import Address

class AddressResource(ModelResource):
    class Meta:
        queryset = Address.objects.all()
        fields = []
        list_allowed_methods = []
        detail_allowed_methods = []