from tastypie import fields
from tastypie.resources import ModelResource
from data.models import Album

from event import EventResource

class AlbumResource(ModelResource):

    event = fields.ForeignKey(EventResource, 'event')

    class Meta:
        queryset = Album.objects.all()
        fields = ['short_name', 'name', 'description', 'creation_date']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True