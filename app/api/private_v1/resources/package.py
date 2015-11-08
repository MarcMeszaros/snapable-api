# django/tastypie/libs
from tastypie import fields
from tastypie.resources import ALL

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Package


class PackageResource(BaseModelResource):

    # DEPRECATED
    # old "enabled" flag (2014-08-04)
    enabled = fields.BooleanField(attribute='is_enabled', default=False)

    class Meta(BaseMeta):  # set Meta to the public API Meta
        queryset = Package.objects.filter(is_enabled=True)
        fields = [
            'short_name',
            'name',
            'amount',
            'items',
            'interval',
            'interval_count',
            'is_enabled',
            'trial_period_days',
            # DEPRECATED
            'enabled'
        ]
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            'is_enabled': ['exact'],
            'short_name': ALL,
            # DEPRECATED
            'enabled': ['exact'],
        }

    def dehydrate(self, bundle):
        # small hack required to make the field return as json
        bundle.data['items'] = bundle.obj.items

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['price'] = bundle.obj.amount

        return bundle
