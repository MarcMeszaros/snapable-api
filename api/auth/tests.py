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
        self.key = 'abc123'
        self.secret = 'abc'

        #rf = RequestFactory()
        #self.get_request = rf.get('/private_v1/event/')
        #self.post_request = rf.post('/private_v1/event/', {'foo': 'bar'})
        
    def test_create_signature(self):
        signature = ServerAuthentication.create_signature(self.key, self.secret, 'GET', '/private_v1/event/')
        expected_timestamp = time.strftime('%s', time.gmtime())

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
        snap_timestamp = auth_params['snap_timestamp']
        raw = self.key + 'GET' + '/private_v1/event/' + snap_nonce + snap_timestamp
        expected_signature = hmac.new(self.secret, raw, hashlib.sha1).hexdigest()

        # assert the timestamp matched
        self.assertEqual(snap_timestamp, expected_timestamp)

        # assert the signature is correct
        self.assertEqual(signature, expected_signature)

    def test_create_signature_legacy(self):
        signature = ServerAuthentication.create_signature(self.key, self.secret, 'GET', '/private_v1/event/', True)
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
        raw = self.key + 'GET' + '/private_v1/event/' + snap_nonce + snap_date
        expected_signature = hmac.new(self.secret, raw, hashlib.sha1).hexdigest()

        # assert the timestamp matched
        self.assertEqual(snap_date, expected_date)

        # assert the signature is correct
        self.assertEqual(signature, expected_signature)