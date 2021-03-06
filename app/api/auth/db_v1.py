# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0301,F0401
import hashlib
import hmac
import os
import pickle
import time
from datetime import datetime, timedelta

# django/tastypie/libs
import envitro
import pytz
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, Unauthorized

# snapable
import api.auth
import data.models
import utils.redis
from api.models import ApiKey

SNAP_AUTHENTICATION = envitro.bool('SNAP_AUTHENTICATION', True)
SNAP_AUTHORIZATION = envitro.bool('SNAP_AUTHORIZATION', True)


def get_api_key(key):
    try:
        redis_key = 'api_key_{0}'.format(key)
        utils.redis.client.expire(redis_key, 900)  # update the ttl if possible
        api_redis_string = utils.redis.client.get(redis_key)  # get the key
        if api_redis_string:
            api_key = pickle.loads(api_redis_string)
            return api_key
        else:
            api_key = ApiKey.objects.get(key=key)
            api_redis_string = pickle.dumps(api_key)
            utils.redis.client.setex(redis_key, 900, api_redis_string)
            return api_key
    except:
        return ApiKey.objects.get(key=key)


def apiAuthorizationChecks(request):
    auth_params = api.auth.get_auth_params(request)
    api_key = get_api_key(auth_params['key'])
    version = request.META['PATH_INFO'].strip('/').split('/')[0]

    if not api_key.is_enabled:
        raise Unauthorized('This API key is unauthorized.')

    if version != str(api_key.version) and version != 'control_tower':
        raise Unauthorized('Not authorized to access this API.')


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
        sanitized_uri = uri.split('?', 1)[0]
        raw = api_key + method + sanitized_uri + snap_nonce + snap_timestamp
        signature = hmac.new(api_secret, raw, hashlib.sha1).hexdigest()
        return 'SNAP key="{0}",signature="{1}",nonce="{2}",timestamp="{3}"'.format(api_key, signature, snap_nonce, snap_timestamp)

    @staticmethod
    def sign_request(request, api_key, api_secret):
        request.META['HTTP_AUTHORIZATION'] = DatabaseAuthentication.create_signature(api_key, api_secret, request.method, request.path)
        return request

    def is_authenticated(self, request, **kwargs):
        # check for the environment variable to skip auth
        if not SNAP_AUTHENTICATION:
            return True

        try:
            # get the Authorization header
            auth = request.META['HTTP_AUTHORIZATION'].strip().split(' ')
            auth_snap = auth[0].lower()

            # get signature info from the Authorization header
            auth_params = api.auth.get_auth_params(request)

            # add the parts to proper varibles for signature
            api_key = get_api_key(auth_params['key'])
            signature = auth_params['signature']
            snap_nonce = auth_params['nonce']
            snap_timestamp = auth_params['timestamp']

            # create the raw string to hash and calculate hashed value
            raw = api_key.key + request.method + request.path + snap_nonce + snap_timestamp
            hashed = hmac.new(str(api_key.secret), raw, hashlib.sha1)

            # calculate time differences
            snap_datetime = datetime.fromtimestamp(int(snap_timestamp), tz=pytz.utc) # parse the date header
            now_datetime = datetime.now(pytz.utc) # current time on server
            pre_now_datetime = now_datetime + timedelta(0, -300) # 5 minutes in the past
            post_now_datetime = now_datetime + timedelta(0, 300) # 5 minutes in the future

            # time check
            if snap_datetime < pre_now_datetime or snap_datetime > post_now_datetime:
                raise BadRequest('Timestamp must be within +/- 5mins from Snapable API server clock.')

            # if all conditions pass, return true
            if auth_snap == 'snap' and signature == hashed.hexdigest():
                return True
            else:
                return False  # we failed, return false
        except KeyError:
            raise BadRequest('Missing authentication param')
        except ApiKey.DoesNotExist:
            raise BadRequest('The API key does not exist')

    # Optional but recommended
    def get_identifier(self, request):
        auth_params = api.auth.get_auth_params(request)
        return get_api_key(auth_params['key'])


class DatabaseAuthorization(Authorization):

    def create_detail(self, object_list, bundle):
        # check for the environment variable to skip auth
        if not SNAP_AUTHORIZATION:
            return True

        # check if authorized to access the API and get the API key
        apiAuthorizationChecks(bundle.request)
        api_key = DatabaseAuthentication().get_identifier(bundle.request)

        if api_key.permission_mask.create:
            return True
        else:
            raise Unauthorized('Not authorized to create resource.')

    def read_list(self, object_list, bundle):
        if not SNAP_AUTHORIZATION:
            return True

        # check if authorized to access the API and get the API key
        apiAuthorizationChecks(bundle.request)
        api_key = DatabaseAuthentication().get_identifier(bundle.request)

        # no read permission, return empty list
        if not api_key.permission_mask.read:
            raise Unauthorized('Not authorized to read resource.')

        # empty list or private API account, allowed to access all objects
        if len(object_list) <= 0 or api_key.version[:7] == 'private':
            return object_list

        # filter objects as required
        if isinstance(object_list[0], data.models.Account):
            return object_list.filter(api_account=api_key.account)
        elif isinstance(object_list[0], data.models.Event):
            return object_list.filter(account__api_account=api_key.account)
        elif isinstance(object_list[0], data.models.Guest):
            return object_list.filter(event__account__api_account=api_key.account)
        elif isinstance(object_list[0], data.models.Location):
            return object_list.filter(event__account__api_account=api_key.account)
        elif isinstance(object_list[0], data.models.Photo):
            return object_list.filter(event__account__api_account=api_key.account)
        elif isinstance(object_list[0], data.models.User):
            return object_list.filter(account__api_account=api_key.account)
        else:
            return []

    def read_detail(self, object_list, bundle):
        # disable schema to be read
        if 'schema' in bundle.request.path and bundle.request.path.split('/')[-2] == 'schema':
            return False

        # check for the environment variable to skip auth
        if not SNAP_AUTHORIZATION:
            return True

        # check if authorized to access the API and get the API key
        apiAuthorizationChecks(bundle.request)
        api_key = DatabaseAuthentication().get_identifier(bundle.request)

        # no read permission, return false
        if not api_key.permission_mask.read:
            raise Unauthorized('Not authorized to read resource.')

        # private API account, allowed to access all objects
        if api_key.version[:7] == 'private':
            return True

        # filter objects as required
        if isinstance(bundle.obj, data.models.Account):
            return matching_api_account(bundle.obj.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Event):
            return matching_api_account(bundle.obj.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Guest):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Location):
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
        raise Unauthorized('Bulk updates are not permitted.')

    def update_detail(self, object_list, bundle):
        # check for the environment variable to skip auth
        if not SNAP_AUTHORIZATION:
            return True

        # check if authorized to access the API and get the API key
        apiAuthorizationChecks(bundle.request)
        api_key = DatabaseAuthentication().get_identifier(bundle.request)

        # no update permission, return false
        if not api_key.permission_mask.update:
            raise Unauthorized('Not authorized to update resource.')

        # private API account, allowed to access all objects
        if api_key.version[:7] == 'private':
            return True

        # filter objects as required
        if isinstance(bundle.obj, data.models.Account):
            return matching_api_account(bundle.obj.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Event):
            return matching_api_account(bundle.obj.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Guest):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Location):
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
        raise Unauthorized('Bulk deletes are not permitted.')

    def delete_detail(self, object_list, bundle):
        # check for the environment variable to skip auth
        if not SNAP_AUTHORIZATION:
            return True

        # check if authorized to access the API and get the API key
        apiAuthorizationChecks(bundle.request)
        api_key = DatabaseAuthentication().get_identifier(bundle.request)

        # no delete permission, return false
        if not api_key.permission_mask.delete:
            raise Unauthorized('Not authorized to delete resource.')

        # private API account, allowed to access all objects
        if api_key.version[:7] == 'private':
            return True

        # filter objects as required
        if isinstance(bundle.obj, data.models.Account):
            return matching_api_account(bundle.obj.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Event):
            return matching_api_account(bundle.obj.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Guest):
            return matching_api_account(bundle.obj.event.account.api_account, api_key.account)
        elif isinstance(bundle.obj, data.models.Location):
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
