from tastypie.resources import ModelResource
from data.models import Package

class PackageResource(ModelResource):
    class Meta:
        queryset = Package.objects.all()
        fields = [
            'short_name', 
            'name', 
            'price', 
            'items'
        ]
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True

    def dehydrate(self, bundle):
        # small hack required to make the field return as json
        bundle.data['items'] = bundle.obj.items

        return bundle