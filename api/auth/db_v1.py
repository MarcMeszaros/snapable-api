# python
import dateutil.parser
import hashlib
import hmac
import random
import time

from datetime import datetime, timedelta

# django/tastypie/libs
import pytz

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, Unauthorized

# snapable
import api.auth
import data.models

from api.models import ApiKey

def isAuthorizedApiVersion(request):
    auth_params = api.auth.get_auth_params(request)
    api_key = ApiKey.objects.get(key=auth_params['key'])
    version = request.META['PATH_INFO'].strip('/').split('/')[0]

    if version == str(api_key.version) and api_key.enabled:
        return True
    else:
        return False

def matching_api_account(first, second):
    if first == second:
        return True
    else:
        raise Unauthorized('Not authorized to access resource.')

class DatabaseAuthentication(Authentication):

    @staticmethod
    def create_signature(api_key, api_secret, method, uri):
        # add the parts to proper varibles for signature
        snap_nonce = api.auth.get_nonce()
        snap_timestamp = time.strftime('%s', time.localtime())
        raw = api_key + method + uri + snap_nonce + snap_timestamp
        signature = hmac.new(api_secret, raw, hashlib.sha1).hexdigest()
        return 'SNAP key="'+api_key+'",signature="'+signature+'",nonce="'+snap_nonce+'",timestamp="'+snap_timestamp+'"'

    def is_authenticated(self, request, **kwargs):
        try:
            # get the Authorization header
            auth = request.META['HTTP_AUTHORIZATION'].strip().split(' ')
            auth_snap = auth[0].lower()
            
            # get the request verb and path
            request_method = request.META['REQUEST_METHOD']
            request_path = request.path

            # get signature info from the Authorization header
            auth_params = api.auth.get_auth_params(request)

            # add the parts to proper varibles for signature
            key = auth_params['key']
            api_key = ApiKey.objects.get(key=key)
            secret = str(api_key.secret)
            signature = auth_params['signature']
            x_snap_nonce = auth_params['nonce']
            x_snap_timestamp = auth_params['timestamp']

            # create the raw string to hash
            raw = key + request_method + request_path + x_snap_nonce + x_snap_timestamp

            # calculate the hash
            hashed = hmac.new(secret, raw, hashlib.sha1)

            # calculate time differences
            x_snap_datetime = datetime.fromtimestamp(int(x_snap_timestamp), tz=pytz.utc)# parse the date header
            now_datetime = datetime.now(pytz.utc) # current time on server
            pre_now_datetime = now_datetime + timedelta(0, -300) # 5 minutes in the past
            post_now_datetime = now_datetime + timedelta(0, 300) # 5 minutes in the future

            # if all conditions pass, return true
            if auth_snap == 'snap' and (x_snap_datetime >= pre_now_datetime and x_snap_datetime <= post_now_datetime) and signature == hashed.hexdigest():
                return True
            else:
                return False # we failed, return false
        except KeyError as e:
            raise BadRequest('Missing authentication param')
        except ApiKey.DoesNotExist as e:
            raise BadRequest('The API key does not exist')

    # Optional but recommended
    def get_identifier(self, request):
        auth_params = api.auth.get_auth_params(request)
        return ApiKey.objects.get(key=auth_params['key'])

class DatabaseAuthorization(Authorization):

    def create_detail(self, object_list, bundle):
        # check if authorized to access the API
        if not isAuthorizedApiVersion(bundle.request):
            raise Unauthorized('Not authorized to access API.')

        # get the API key
        api_key = DatabaseAuthentication().get_identifier(bundle.request)
        if api_key.enabled == False:
            raise Unauthorized('This API key is unauthorized.')

        return True

    def read_list(self, object_list, bundle):
        # check if authorized to access the API
        if not isAuthorizedApiVersion(bundle.request):
            raise Unauthorized('Not authorized to access API.')

        # get the API key
        api_key = DatabaseAuthentication().get_identifier(bundle.request)
        if api_key.enabled == False:
            raise Unauthorized('This API key is unauthorized.')

        # filter objects as required
        if isinstance(object_list[0], data.models.Account):
            return object_list.filter(api_account=api_key.account)
        elif isinstance(object_list[0], data.models.Address):
            return object_list.filter(event__account__api_account=api_key.account)
        elif isinstance(object_list[0], data.models.Event):
            return object_list.filter(account__api_account=api_key.account)
        elif isinstance(object_list[0], data.models.Guest):
            return object_list.filter(event__account__api_account=api_key.account)
        elif isinstance(object_list[0], data.models.Photo):
            return object_list.filter(event__account__api_account=api_key.account)
        elif isinstance(object_list[0], data.models.User):
            return object_list.filter(account__api_account=api_key.account)
        else:
            return []

    def read_detail(self, object_list, bundle):
        # allow schema to be read
        if bundle.request.path.split('/')[-2] == 'schema':
            return True

        # check if authorized to access the API
        if not isAuthorizedApiVersion(bundle.request):
            raise Unauthorized('Not authorized to access API.')

        # get the API key
        api_key = DatabaseAuthentication().get_identifier(bundle.request)
        if api_key.enabled == False:
            raise Unauthorized('This API key is unauthorized.')

        # filter objects as required
        if isinstance(bundle.obj, data.models.Account):
            return matching_api_account(bundle.obj.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Address):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Event):
            return matching_api_account(bundle.obj.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Guest):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Photo):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.User):
            if bundle.obj.account_set.filter(api_account=api_key.account).count() > 0:
                return True
            else:
                return False
        else:
            raise Unauthorized('Not authorized to access resource.')

    def update_list(self, object_list, bundle):
        return [] # No update of lists

    def update_detail(self, object_list, bundle):
        # check if authorized to access the API
        if not isAuthorizedApiVersion(bundle.request):
            raise Unauthorized('Not authorized to access API.')

        # get the API key
        api_key = DatabaseAuthentication().get_identifier(bundle.request)
        if api_key.enabled == False:
            raise Unauthorized('This API key is unauthorized.')

        # filter objects as required
        if isinstance(bundle.obj, data.models.Account):
            return matching_api_account(bundle.obj.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Address):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Event):
            return matching_api_account(bundle.obj.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Guest):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Photo):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.User):
            if bundle.obj.account_set.filter(api_account=api_key.account).count() > 0:
                return True
            else:
                return False
        else:
            raise Unauthorized('Not authorized to access resource.')

    def delete_list(self, object_list, bundle):
        return [] # No delete of lists

    def delete_detail(self, object_list, bundle):
        # check if authorized to access the API
        if not isAuthorizedApiVersion(bundle.request):
            raise Unauthorized('Not authorized to access API.')

        # get the API key
        api_key = DatabaseAuthentication().get_identifier(bundle.request)
        if api_key.enabled == False:
            raise Unauthorized('This API key is unauthorized.')

        # filter objects as required
        if isinstance(bundle.obj, data.models.Account):
            return matching_api_account(bundle.obj.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Address):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Event):
            return matching_api_account(bundle.obj.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Guest):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Photo):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.User):
            if bundle.obj.account_set.filter(api_account=api_key.account).count() > 0:
                return True
            else:
                return False
        else:
            raise Unauthorized('Not authorized to access resource.')
