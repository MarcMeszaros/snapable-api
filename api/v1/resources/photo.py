from tastypie.resources import ModelResource
from data.models import Photo

class PhotoResource(ModelResource):
    class Meta:
        queryset = Photo.objects.all()
        fields = ['caption']
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']