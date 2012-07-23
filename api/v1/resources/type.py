from tastypie import fields
from tastypie.resources import ModelResource
from data.models import Type

class TypeResource(ModelResource):

    class Meta:
        queryset = Type.objects.all()
        fields = []
        list_allowed_methods = []
        detail_allowed_methods = []
        always_return_data = True