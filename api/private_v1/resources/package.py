# django/tastypie/libs
from tastypie.resources import ALL

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Package

class PackageResource(BaseModelResource):

    class Meta(BaseMeta): # set Meta to the public API Meta
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
        filtering = {
            'short_name': ALL,
            'enabled': ['exact'],
        }

    def dehydrate(self, bundle):
        # small hack required to make the field return as json
        bundle.data['items'] = bundle.obj.items

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['price'] = bundle.obj.amount

        return bundle