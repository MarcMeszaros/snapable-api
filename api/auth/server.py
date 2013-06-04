# python
import dateutil.parser
import hashlib
import hmac
import random
import re
import time

# django/tastypie/libs
import pytz

from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, Unauthorized

# snapable
import api.auth

from data.models import PasswordNonce, User

def legacyIsAuthorized(request):
    try:
        if 'HTTP_X_SNAP_USER' not in request.META and (request.method in ['GET', 'POST']):
            return True
        else:
            # get the header data
            x_snap_user = request.META['HTTP_X_SNAP_USER']
            user_details = x_snap_user.strip().split(':')

            # get the user model matching the email
            user = User.objects.get(email=user_details[0])
            nonce = PasswordNonce.objects.get(user=user, valid=True, nonce=user_details[1])

            # get the matched user's password data
            db_pass = user.password.split('$', 1)
            pass_data = {}

            # various data based on db_pass type
            if db_pass[0] == 'bcrypt':
                pass_data['password_algorithm'] = db_pass[0]
                pass_data['password_data'] = db_pass[1]

            elif db_pass[0] == 'pbkdf2_sha256':
                pass_parts = db_pass[1].split('$')
                pass_data['password_hash'] = pass_parts[2]

            # if the db password hash and the one in the header match, display the user details
            if pass_data['password_hash'] == user_details[1]:
                return True
            elif (nonce.valid):
                nonce.valid = False # invalidate the nonce so it can't be used again 
                # WEIRDness... uncomment and the function returns 'None',
                # comment it and it works...
                # nonce.save()
                return True
            else:
                return False

    except:
        return False

class ServerAuthentication(Authentication):

    @staticmethod
    def create_signature(api_key, api_secret, method, uri, legacy=False):
        # add the parts to proper varibles for signature
        snap_nonce = api.auth.get_nonce()
        if not legacy:
            snap_timestamp = time.strftime('%s', time.localtime())
            raw = api_key + method + uri + snap_nonce + snap_timestamp
            signature = hmac.new(api_secret, raw, hashlib.sha1).hexdigest()
            return 'SNAP key="'+api_key+'",signature="'+signature+'",nonce="'+snap_nonce+'",timestamp="'+snap_timestamp+'"'
        else:
            snap_date = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
            raw = api_key + method + uri + snap_nonce + snap_date
            signature = hmac.new(api_secret, raw, hashlib.sha1).hexdigest()
            return 'SNAP snap_key="'+api_key+'",snap_signature="'+signature+'",snap_nonce="'+snap_nonce+'",snap_date="'+snap_date+'"'

    def is_authenticated(self, request, **kwargs):
        try:
            # get the Authorization header
            auth = request.META['HTTP_AUTHORIZATION'].strip().split(' ')
            auth_snap = auth[0].lower()

            # get the request verb and path
            request_method = request.META['REQUEST_METHOD']
            request_path = request.path

            if 'signature' in auth[1]:
                # get signature info all in Authorization header
                auth_parts = auth[1].strip().split(',')
                auth_params = dict()
                for part in auth_parts:
                    items = part.replace('"','').split('=')
                    auth_params[items[0]] = items[1]

                # add the parts to proper varibles for signature
                try:
                    key = auth_params['key']
                except:
                    key = auth_params['snap_key'] # deprecated(2013-05-10) kept for compatibility
                try:
                    signature = auth_params['signature']
                except:
                    signature = auth_params['snap_signature'] # deprecated(2013-05-10) kept for compatibility
                try:
                    x_snap_nonce = auth_params['nonce']
                except:
                    x_snap_nonce = auth_params['snap_nonce'] # deprecated(2013-05-10) kept for compatibility
                try:
                    x_snap_timestamp = auth_params['timestamp']
                except:
                    # deprecated(2013-05-10) kept for compatibility
                    if 'snap_timestamp' in auth_params:
                        x_snap_timestamp = auth_params['snap_timestamp']
                    else:
                        x_snap_date = auth_params['snap_date']

                try:
                    secret = settings.APIKEY[key]
                except KeyError:
                    return False

            # deprecated but kept for compatibility
            else:
                # api signature info in multiple headers
                key = auth[1].split(':')[0]
                try:
                    secret = settings.APIKEY[key]
                except KeyError:
                    return False
                signature = auth[1].split(':')[1]
                x_snap_nonce = request.META['HTTP_X_SNAP_NONCE']
                x_snap_date = request.META['HTTP_X_SNAP_DATE']

            # create the raw string to hash
            try:
                raw = key + request_method + request_path + x_snap_nonce + x_snap_timestamp
            except:
                raw = key + request_method + request_path + x_snap_nonce + x_snap_date

            # calculate the hash
            hashed = hmac.new(secret, raw, hashlib.sha1)

            # calculate time differences
            try:
                x_snap_datetime = datetime.fromtimestamp(int(x_snap_timestamp), tz=pytz.utc)
            except:
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
            raise BadRequest('Missing authentication param: '+str(e))

class ServerAuthorization(Authorization):
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
        if legacyIsAuthorized(bundle.request):
            return True
        else:
            raise Unauthorized("Sorry, no update.")

    def delete_list(self, object_list, bundle):
        return []

    def delete_detail(self, object_list, bundle):
        return legacyIsAuthorized(bundle.request)
    