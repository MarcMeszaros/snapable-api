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

from data.models import User

class ServerAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        # if in debug mode, always authenticate
        if settings.DEBUG_AUTHENTICATION == True:
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
        # if in debug mode, always authenticate
        if settings.DEBUG_AUTHORIZATION == True:
            return True

        if not 'HTTP_X_SNAP_USER' in request.META and (request.method in ['GET', 'POST']):
            return True

        try:
            # get the header data
            x_snap_user = request.META['HTTP_X_SNAP_USER']
            user_details = x_snap_user.strip().split(':')

            # get the user model matching the email
            user = User.objects.get(email=user_details[0])

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
            else:
                return False

        except:
            return False

    # Optional but useful for advanced limiting, such as per user.
    def apply_limits(self, request, object_list):
        if request and 'HTTP_X_SNAP_USER' in request.META:
            # get the header data
            x_snap_user = request.META['HTTP_X_SNAP_USER']
            user_details = x_snap_user.strip().split(':')

            # apply filtering based on different query sets
            if len(object_list) > 0 and isinstance(object_list[0], User):
                return object_list.filter(email=user_details[0])
            else:
                return object_list

        return object_list