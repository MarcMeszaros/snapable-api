# django/tastypie/libs
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.validation import Validation

# snapable
import api.auth
import api.base_v1.resources

from data.models import Event
from event import EventResource

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

class LocationResource(api.base_v1.resources.AddressResource):

    event = fields.ToOneField(EventResource, 'event', null=True)

    class Meta(api.base_v1.resources.AddressResource.Meta): # set Meta to the public API Meta
        fields = api.base_v1.resources.AddressResource.Meta.fields + ['address', 'lat', 'lng']
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        authentication = api.auth.DatabaseAuthentication()
        authorization = api.auth.DatabaseAuthorization()
        validation = LocationValidation()
        filtering = {
            'event': ['exact'],
        }
