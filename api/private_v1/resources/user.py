import api.v1.resources
from tastypie.authorization import Authorization

class UserResource(api.v1.resources.UserResource):

    Meta = api.v1.resources.UserResource.Meta # set Meta to the public API Meta
    Meta.fields += ['password', 'billing_zip', 'terms', 'id']
    Meta.list_allowed_methods += ['post']
    Meta.authorization = Authorization()

    def __init__(self):
        api.v1.resources.UserResource.__init__(self)