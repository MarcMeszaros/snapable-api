from tastypie.resources import ModelResource
from data.models import Location

class AddressResource(ModelResource):
    class Meta:
        queryset = Location.objects.all()
        fields = []
        list_allowed_methods = []
        detail_allowed_methods = []