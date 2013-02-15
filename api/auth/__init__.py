# Authentication
from api.auth.db_v1 import DatabaseAuthentication
from api.auth.server import ServerAuthentication

# Authorization
from api.auth.db_v1 import DatabaseAuthorization
from api.auth.server import ServerAuthorization

# helper funtion
def getAuthParams(request):
    auth = request.META['HTTP_AUTHORIZATION'].strip().split(' ')
    auth_snap = auth[0].lower()
    auth_parts = auth[1].strip().split(',')

    auth_params = dict()
    for part in auth_parts:
        items = part.replace('"','').split('=')
        auth_params[items[0].lower()] = items[1]

    return auth_params