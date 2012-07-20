from tastypie.resources import ModelResource
from data.models import Event

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        fields = ['user_id', 'start', 'end', 'title', 'url', 'pin', 'creation_date', 'enabled']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True