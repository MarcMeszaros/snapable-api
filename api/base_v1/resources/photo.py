from tastypie import fields
from tastypie.resources import ModelResource
from data.models import AlbumPhoto, Photo

from event import EventResource
#from guest import GuestResource

class PhotoResource(ModelResource):
    
    event = fields.ForeignKey(EventResource, 'event')
    #guest = fields.ForeignKey(GuestResource, 'guest')

    class Meta:
        queryset = Photo.objects.all().order_by('-created_at')
        fields = ['caption', 'streamable', 'created_at']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {}