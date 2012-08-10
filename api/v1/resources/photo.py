from tastypie import fields
from tastypie.resources import ModelResource
from data.models import AlbumPhoto, Photo

from event import EventResource
#from guest import GuestResource
from type import TypeResource

class PhotoResource(ModelResource):
    
    event = fields.ForeignKey(EventResource, 'event')
    #guest = fields.ForeignKey(GuestResource, 'guest')
    #type = fields.ForeignKey(TypeResource, 'type')

    class Meta:
        queryset = Photo.objects.all()
        fields = ['caption', 'streamable', 'timestamp']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {}