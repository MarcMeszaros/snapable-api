import dateutil.parser
import hashlib
import hmac
import pytz

from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest
from tastypie.exceptions import Unauthorized

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

class DatabaseAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # if in debug mode, always authenticate
        if settings.DEBUG_AUTHENTICATION == True:
            return True

        try:
            # get the Authorization header
            auth = request.META['HTTP_AUTHORIZATION'].strip().split(' ')
            auth_snap = auth[0].lower()
            
            # get the request verb and path
            request_method = request.META['REQUEST_METHOD']
            request_path = request.path

            # get signature info from the Authorization header
            auth_params = getAuthParams(request)

            # add the parts to proper varibles for signature
            key = auth_params['snap_key']
            api_key = ApiKey.objects.get(key=key)
            secret = str(api_key.secret)
            signature = auth_params['snap_signature']
            x_snap_nonce = auth_params['snap_nonce']
            x_snap_date = auth_params['snap_date']

            # create the raw string to hash
            raw = key + request_method + request_path + x_snap_nonce + x_snap_date

            # calculate the hash
            hashed = hmac.new(secret, raw, hashlib.sha1)

            # calculate time differences
            x_snap_datetime = dateutil.parser.parse(x_snap_date) # parse the date header
            now_datetime = datetime.now(pytz.utc) # current time on server
            pre_now_datetime = now_datetime + timedelta(0, -120) # 2 minutes in the past
            post_now_datetime = now_datetime + timedelta(0, 120) # 2 minutes in the future

            # if all conditions pass, return true
            if auth_snap == 'snap' and (x_snap_datetime >= pre_now_datetime and x_snap_datetime <= post_now_datetime) and signature == hashed.hexdigest():
                return True
            else:
                return False # we failed, return false
        except KeyError as e:
            raise BadRequest('Missing authentication param')

class DatabaseAuthorization(Authorization):
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
