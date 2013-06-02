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
        fields = ['start', 'end', 'tz_offset', 'title', 'url', 'pin', 'enabled', 'public']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        ordering = []
        always_return_data = True
        filtering = {
            'url': ALL,
        }

    def dehydrate_end(self, bundle):
        return bundle.data['end'].strftime('%Y-%m-%dT%H:%M:%SZ')

    def dehydrate_start(self, bundle):
        return bundle.data['start'].strftime('%Y-%m-%dT%H:%M:%SZ')