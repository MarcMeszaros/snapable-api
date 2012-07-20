from tastypie import fields
from tastypie.resources import ModelResource
from data.models import Event

from user import UserResource

class EventResource(ModelResource):

    creator = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Event.objects.all()
        fields = ['start', 'end', 'title', 'url', 'pin', 'creation_date', 'enabled']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True