from tastypie import fields
from tastypie.resources import ALL, ModelResource
from data.models import Event

from user import UserResource

class EventResource(ModelResource):

    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Event.objects.all()
        fields = ['start', 'end', 'tz_offset', 'title', 'url', 'pin', 'creation_date', 'enabled', 'public']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        ordering = []
        always_return_data = True
        filtering = {
            'url': ALL,
        }