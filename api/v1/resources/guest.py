from tastypie import fields
from tastypie.resources import ALL, ModelResource
from data.models import Guest

from event import EventResource
from type import TypeResource

class GuestResource(ModelResource):

    event = fields.ForeignKey(EventResource, 'event')
    type = fields.ForeignKey(TypeResource, 'type')

    class Meta:
        queryset = Guest.objects.all()
        fields = ['name', 'email']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
            'event': ['exact'],
            'email': ALL,
        }
