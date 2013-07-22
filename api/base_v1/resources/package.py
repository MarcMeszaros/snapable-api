from tastypie.resources import ModelResource
from data.models import Package

class PackageResource(ModelResource):
    class Meta:
        queryset = Package.objects.filter(enabled=True)
        fields = [
            'short_name', 
            'name', 
            'amount', 
            'items',
            'interval',
            'interval_count',
            'trial_period_days',
            'enabled'
        ]
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True

    def dehydrate(self, bundle):
        # small hack required to make the field return as json
        bundle.data['items'] = bundle.obj.items

        return bundle