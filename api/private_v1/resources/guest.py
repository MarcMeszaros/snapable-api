# django/tastypie/libs
from tastypie import fields
from tastypie.resources import ALL

# snapable
from .meta import BaseMeta, BaseModelResource
from data.models import Guest

class GuestResource(BaseModelResource):

    event = fields.ForeignKey('api.private_v1.resources.EventResource', 'event')

    # DEPRECATED
    # old "invited" flag (2014-07-16)
    invited = fields.BooleanField(attribute='is_invited', default=False)

    class Meta(BaseMeta): # set Meta to the public API Meta
        queryset = Guest.objects.all()
        fields = [
            'name', 'email', 'is_invited',
            # DEPRECATED
            'invited',
        ]
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        filtering = {
            'event': ['exact'],
            'email': ALL,
            'is_invited': ALL,
            # DEPRECATED
            'invited': ALL,
        }

    def dehydrate(self, bundle):

        ### DEPRECATED/COMPATIBILITY ###
        bundle.data['type'] = '/private_v1/type/6/'

        return bundle
