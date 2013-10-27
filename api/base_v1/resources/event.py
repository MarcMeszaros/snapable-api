# django/tastypie/libs
from tastypie import fields
from tastypie.resources import ALL, ModelResource

# snapable
from data.models import Event
from user import UserResource

class EventResource(ModelResource):

    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Event.objects.all()
        fields = ['start_at', 'end_at', 'tz_offset', 'title', 'url', 'pin', 'is_enabled', 'is_public']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        ordering = []
        always_return_data = True
        filtering = {
            'url': ALL,
        }

    def dehydrate_end_at(self, bundle):
        return bundle.data['end_at'].strftime('%Y-%m-%dT%H:%M:%SZ')

    def dehydrate_start_at(self, bundle):
        return bundle.data['start_at'].strftime('%Y-%m-%dT%H:%M:%SZ')