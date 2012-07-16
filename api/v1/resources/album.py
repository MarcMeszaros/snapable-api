from tastypie.resources import ModelResource
from data.models import Album

class AlbumResource(ModelResource):
    class Meta:
        queryset = Album.objects.all()
        fields = ['short_name', 'name']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']