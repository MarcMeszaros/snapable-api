from tastypie.resources import ModelResource
from data.models import Package

class PackageResource(ModelResource):
    class Meta:
        queryset = Package.objects.all()
        fields = [
            'short_name', 
            'name', 
            'price', 
            'prints', 
            'additional_price_per_print', 
            'albums', 
            'slideshow',
            'shipping',
            'table_cards',
            'guest_reminders'
        ]
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True