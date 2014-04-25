# django/tastypie/libs
from tastypie.resources import ModelResource

# snapable
import api.auth
from api.utils.serializers import SnapSerializer

# defaults for this api version
class BaseMeta(object):
    list_allowed_methods = ['get']
    detail_allowed_methods = ['get']
    always_return_data = True
    authentication = api.auth.ServerAuthentication()
    authorization = api.auth.ServerAuthorization()
    serializer = SnapSerializer(formats=['json', 'jpeg'])

class BaseModelResource(ModelResource):
    pass