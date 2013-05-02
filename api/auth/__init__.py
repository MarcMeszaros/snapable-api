# python
import hashlib
import random

## snapable ##
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

def get_nonce(length=16):
    random_hash = hashlib.sha512(str(random.SystemRandom().getrandbits(512))).hexdigest()
    if length >= 16:
        return random_hash[:length]
    else:
        return random_hash[:16]