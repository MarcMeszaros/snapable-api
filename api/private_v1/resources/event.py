import api.auth
import api.v1.resources
import copy

from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tastypie import fields
from tastypie.authorization import Authorization

from package import PackageResource
from type import TypeResource
from user import UserResource

from data.models import Address
from data.models import Event

class EventResource(api.v1.resources.EventResource):

    user = fields.ForeignKey(UserResource, 'user')
    package = fields.ForeignKey(PackageResource, 'package')
    type = fields.ForeignKey(TypeResource, 'type')

    Meta = api.v1.resources.EventResource.Meta # set Meta to the public API Meta
    Meta.fields += []
    Meta.list_allowed_methods = ['get', 'post']
    Meta.detail_allowed_methods = ['get', 'post', 'put', 'delete']
    Meta.authentication = api.auth.ServerAuthentication()
    Meta.authorization = Authorization()
    Meta.filtering = dict(Meta.filtering, **{
        'enabled': ['exact'],
        'user': ['exact'], 
    })

    def __init__(self):
        api.v1.resources.EventResource.__init__(self)

    def dehydrate(self, bundle):

        # try and add address info
        try:
            # get all addresses for the event
            db_addresses = Address.objects.filter(event_id=bundle.obj.id)
            
            # add the addresses for the event
            json_addresses = []
            for obj in db_addresses:
                json_addresses.append({
                    'address': obj.address,
                    'lat': obj.lat,
                    'lng': obj.lng,
                })

            # append the addresses to the json response
            bundle.data['addresses'] = json_addresses
        except ObjectDoesNotExist:
            pass

        return bundle
