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

from api.models import ApiKey

def getAuthParams(request):
    auth = request.META['HTTP_AUTHORIZATION'].strip().split(' ')
    auth_snap = auth[0].lower()
    auth_parts = auth[1].strip().split(',')

    auth_params = dict()
    for part in auth_parts:
        items = part.replace('"','').split('=')
        auth_params[items[0]] = items[1]

    return auth_params

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

            if "snap_signature" in auth[1]:
                # get signature info all in Authorization header
                auth_parts = auth[1].strip().split(',')
                auth_params = dict()
                for part in auth_parts:
                    items = part.replace('"','').split('=')
                    auth_params[items[0]] = items[1]

                # add the parts to proper varibles for signature
                key = auth_params['snap_key']
                secret = str(ApiKey.objects.get(key=key).secret)
                signature = auth_params['snap_signature']
                x_snap_nonce = auth_params['snap_nonce']
                x_snap_date = auth_params['snap_date']

            else:
                # api signature info in multiple headers
                key = auth[1].split(':')[0]
                secret = str(ApiKey.objects.get(key=key).secret)
                signature = auth[1].split(':')[1]
                x_snap_nonce = request.META['HTTP_X_SNAP_NONCE']
                x_snap_date = request.META['HTTP_X_SNAP_DATE']

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

            # we failed, return false
            return False
        except KeyError as e:
            print request
            print e
            return False

class DatabaseAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        auth_params = getAuthParams(request)
        api_key = ApiKey.objects.get(key=auth_params['snap_key'])
        version = request.META['PATH_INFO'].strip('/').split('/')[0]

        if version == str(api_key.version):
            return True
        else:
            return False
