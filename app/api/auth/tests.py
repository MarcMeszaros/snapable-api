# python
import datetime
import hashlib
import hmac
import time

# django/tastypie
from django.test import (RequestFactory, TestCase)

# snapable
from api.auth.server import ServerAuthentication

class ServerAuthenticationTest(TestCase):

    def setUp(self):
        self.key = 'key123'
        self.secret = 'sec123'
        self.auth = ServerAuthentication()

        self.uri = '/private_v1/event/'
        self.rf = RequestFactory()
        
        self.get_request = self.rf.get(self.uri)
        self.get_request.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature(self.key, self.secret, 'GET', self.uri)
        self.get_request_legacy = self.rf.get(self.uri)
        self.get_request_legacy.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature(self.key, self.secret, 'GET', self.uri, True)

        self.post_request = self.rf.post(self.uri, {'foo': 'bar'})
        
    def test_create_signature(self):
        signature = ServerAuthentication.create_signature(self.key, self.secret, 'GET', self.uri)
        expected_timestamp = time.strftime('%s', time.gmtime())

        # expected
        auth = signature.strip().split(' ')
        auth_parts = auth[1].strip().split(',')
        auth_params = dict()
        for part in auth_parts:
            items = part.replace('"','').split('=')
            auth_params[items[0]] = items[1]

        # add the parts to proper varibles for signature
        signature = auth_params['signature']
        snap_nonce = auth_params['nonce']
        snap_timestamp = auth_params['timestamp']
        raw = self.key + 'GET' + self.uri + snap_nonce + snap_timestamp
        expected_signature = hmac.new(self.secret, raw, hashlib.sha1).hexdigest()

        # assert the timestamp matched
        self.assertEqual(snap_timestamp, expected_timestamp)

        # assert the signature is correct
        self.assertEqual(signature, expected_signature)

    def test_create_signature_legacy(self):
        signature = ServerAuthentication.create_signature(self.key, self.secret, 'GET', self.uri, True)
        expected_date = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())

        # expected
        auth = signature.strip().split(' ')
        auth_parts = auth[1].strip().split(',')
        auth_params = dict()
        for part in auth_parts:
            items = part.replace('"','').split('=')
            auth_params[items[0]] = items[1]

        # add the parts to proper varibles for signature
        signature = auth_params['snap_signature']
        snap_nonce = auth_params['snap_nonce']
        snap_date = auth_params['snap_date']
        raw = self.key + 'GET' + self.uri + snap_nonce + snap_date
        expected_signature = hmac.new(self.secret, raw, hashlib.sha1).hexdigest()

        # assert the timestamp matched
        self.assertEqual(snap_date, expected_date)

        # assert the signature is correct
        self.assertEqual(signature, expected_signature)

    def test_is_authorized(self):
        self.assertTrue(self.auth.is_authenticated(self.get_request))
        self.assertTrue(self.auth.is_authenticated(self.get_request_legacy))

    def test_is_unauthorized(self):
        # create 2 local copies of the request auths in setup so we don't mess up the values 
        get_request_unauth = self.rf.get(self.uri)
        get_request_unauth_legacy = self.rf.get(self.uri)

        # various permutations of invalid auth
        get_request_unauth.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature('invalidkey', self.secret, 'GET', self.uri)
        self.assertFalse(self.auth.is_authenticated(get_request_unauth))

        get_request_unauth.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature(self.key, 'invalidsecret', 'GET', self.uri)
        self.assertFalse(self.auth.is_authenticated(get_request_unauth))

        get_request_unauth.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature(self.key, self.secret, 'POST', self.uri)
        self.assertFalse(self.auth.is_authenticated(get_request_unauth))

        get_request_unauth.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature(self.key, self.secret, 'GET', '/private_v1/invalid/')
        self.assertFalse(self.auth.is_authenticated(get_request_unauth))

        # various permutations of invalid auth (legacy)
        get_request_unauth_legacy.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature('invalidkey', self.secret, 'GET', self.uri, True)
        self.assertFalse(self.auth.is_authenticated(get_request_unauth_legacy))

        get_request_unauth_legacy.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature(self.key, 'invalidsecret', 'GET', self.uri, True)
        self.assertFalse(self.auth.is_authenticated(get_request_unauth_legacy))

        get_request_unauth_legacy.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature(self.key, self.secret, 'POST', self.uri, True)
        self.assertFalse(self.auth.is_authenticated(get_request_unauth_legacy))

        get_request_unauth_legacy.META['HTTP_AUTHORIZATION'] = ServerAuthentication.create_signature(self.key, self.secret, 'GET', '/private_v1/invalid/', True)
        self.assertFalse(self.auth.is_authenticated(get_request_unauth_legacy))
        
