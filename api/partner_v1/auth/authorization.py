# python/third-party
import dateutil.parser
import hashlib
import hmac
import pytz

# django
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# tastypie
import tastypie.authorization
from tastypie.exceptions import BadRequest
from tastypie.exceptions import Unauthorized

# snapable
from api.models import ApiKey

def getAuthParams(request):
    auth = request.META['HTTP_AUTHORIZATION'].strip().split(' ')
    auth_snap = auth[0].lower()
    auth_parts = auth[1].strip().split(',')

    auth_params = dict()
    for part in auth_parts:
        items = part.replace('"','').split('=')
        auth_params[items[0].lower()] = items[1]

    return auth_params

def legacyIsAuthorized(request):
    # if in debug mode, always authenticate
    if settings.DEBUG_AUTHENTICATION == True:
        return True

    auth_params = getAuthParams(request)
    api_key = ApiKey.objects.get(key=auth_params['snap_key'])
    version = request.META['PATH_INFO'].strip('/').split('/')[0]

    if version == str(api_key.version) and api_key.enabled:
        return True
    else:
        return False

class Authorization(tastypie.authorization.Authorization):
    def create_detail(self, object_list, bundle):
        return legacyIsAuthorized(bundle.request)

    def read_list(self, object_list, bundle):
        if (legacyIsAuthorized(bundle.request)):
            return object_list
        else:
            raise Unauthorized("Sorry, no read.")

    def read_detail(self, object_list, bundle):
        return legacyIsAuthorized(bundle.request)

    def update_list(self, object_list, bundle):
        if (legacyIsAuthorized(bundle.request)):
            return object_list
        else:
            raise Unauthorized("Sorry, no update.")

    def update_detail(self, object_list, bundle):
        return legacyIsAuthorized(bundle.request)

    def delete_list(self, object_list, bundle):
        if (legacyIsAuthorized(bundle.request)):
            return object_list
        else:
            raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        return legacyIsAuthorized(bundle.request)