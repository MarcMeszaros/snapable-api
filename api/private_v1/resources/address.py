import api.v1.resources
from tastypie.authorization import Authorization

class AddressResource(api.v1.resources.AddressResource):

    Meta = api.v1.resources.AddressResource.Meta # set Meta to the public API Meta
    Meta.fields += ['event_id', 'address', 'lat', 'lng']
    Meta.list_allowed_methods += ['get', 'post']
    Meta.detail_allowed_methods += ['get', 'post']
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.AddressResource.__init__(self)
