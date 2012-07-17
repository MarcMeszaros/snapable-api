import api.v1.resources
from tastypie.authorization import Authorization

class EventResource(api.v1.resources.EventResource):

    Meta = api.v1.resources.EventResource.Meta # set Meta to the public API Meta
    Meta.list_allowed_methods += ['post']
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.EventResource.__init__(self)