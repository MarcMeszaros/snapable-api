from tastypie import fields
from tastypie.resources import ModelResource
from data.models import Addon

class AddonResource(ModelResource):

    class Meta:
        queryset = Addon.objects.all()
        fields = ['title', 'description', 'price', 'enabled']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True