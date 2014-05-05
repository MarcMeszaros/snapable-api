# django/tastypie/libs
from tastypie import fields
from tastypie.validation import Validation

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Location

class LocationValidation(Validation):
    def is_valid(self, bundle, request=None):
        errors = {}

        #required = ['address', 'lat', 'lng']
        #for key in required:
        #    try:
        #        bundle.data[key]
        #    except KeyError:
        #        errors[key] = 'Missing field'

        return errors

class LocationResource(BaseModelResource):

    event = fields.ToOneField('api.partner_v1.resources.EventResource', 'event', null=True)

    class Meta(BaseMeta): # set Meta to the public API Meta
        queryset = Location.objects.all()
        fields = ['address', 'lat', 'lng']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        validation = LocationValidation()
        filtering = {
            'event': ['exact'],
        }
