# python
import datetime

# django/tastypie
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase

# snapable
from api.auth.server import ServerAuthentication

class PhotoResourceTest(ResourceTestCase):
    
    def setUp(self):
        super(PhotoResourceTest, self).setUp()
        self.api_key = 'abc123'
        self.api_secret = 'abc'

    def get_credentials(self, method, uri):
        return ServerAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_unauthorized(self):
        method = 'GET'
        uri = '/private_v1/event/'
        self.assertHttpUnauthorized(self.api_client.get(uri, format='json', authentication=ServerAuthentication.create_signature('invalidkey', self.api_secret, method, uri)))
        self.assertHttpUnauthorized(self.api_client.get(uri, format='json', authentication=ServerAuthentication.create_signature(self.api_key, 'invalidsecret', method, uri)))

    def test_create_photo_timestamp(self):
        # not implemented yet
        pass
