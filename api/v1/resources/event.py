from tastypie.resources import ModelResource
from data.models import Event

class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        fields = ['title']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']