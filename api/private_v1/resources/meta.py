# auth
import api.auth

# defaults for this api version
class Meta(object):
    list_allowed_methods = ['get']
    detail_allowed_methods = ['get']
    always_return_data = True
    authentication = api.auth.ServerAuthentication()
    authorization = api.auth.ServerAuthorization()