import dateutil.parser
import hashlib
import hmac
import pytz

from datetime import datetime, timedelta
from django.conf import settings
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest

class ServerAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # if in debug mode, always authenticate
        if settings.DEBUG == True:
            return True

        try:
            # get the Authorization header
            auth = request.META['HTTP_AUTHORIZATION'].strip().split(' ')
            auth_snap = auth[0].lower()
            key = auth[1].split(':')[0]
            secret = settings.APIKEY[key]
            signature = auth[1].split(':')[1]

            # build the signature ourselve
            request_method = request.META['REQUEST_METHOD']
            request_path = request.path
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

class ServerAuthorization(Authorization):
    def is_authorized(self, request, object=None):
            return True