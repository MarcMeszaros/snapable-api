# python
import os
import re

# django/tastypie
from django.conf import settings
from tastypie.test import ResourceTestCase, TestApiClient

# snapable
from api.auth.server import ServerAuthentication
from api.utils.serializers import MultipartSerializer

class Private_v1__PhotoResourceTest(ResourceTestCase):
    fixtures = ['packages.json', 'accounts_and_users.json', 'events.json', 'photos.json']

    def setUp(self):
        super(Private_v1__PhotoResourceTest, self).setUp()
        # we need a custom serializer for multipart uploads
        self.api_client = TestApiClient(serializer=MultipartSerializer())
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        # The data we'll send on POST requests.
        filename = 'trashcat.jpg'
        filepath = os.path.join(settings.PROJECT_PATH, 'api', 'assets', filename)
        f = open(filepath, 'rb')

        self.post_data = {
            'event': '/private_v1/event/1/',
            'caption': 'My super awesome caption!',
            'type': '/private_v1/type/1/',
            'image': {
                'filename': filename,
                'data': f.read(),
            }
        }

    def get_credentials(self, method, uri):
        return ServerAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_post_photo(self):
        uri = '/private_v1/photo/'
        resp = self.api_client.post(uri, data=self.post_data, format='multipart', authentication=self.get_credentials('POST', uri))
        data = self.deserialize(resp)

        # make sure the resource was created
        self.assertHttpCreated(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'author_name',
            'caption',
            'created_at',
            'event',
            'guest',
            'image',
            'resource_uri',
            'streamable',
            'timestamp',
            'type',
        ])

        # make sure the timestamp is in the format we want (ISO8601) without micro
        # expected format: 2013-01-21T18:12:45
        self.assertTrue(re.search('^\d{4}-(\d{2}-?){2}T(\d{2}:?){3}$', data['timestamp']))

    def test_post_photo_noimage(self):
        uri = '/private_v1/photo/'
        del(self.post_data['image'])
        resp = self.api_client.post(uri, data=self.post_data, format='multipart', authentication=self.get_credentials('POST', uri))
        data = self.deserialize(resp)

        # make sure the resource was created
        self.assertHttpBadRequest(resp)

    def test_put_photo(self):
        uri = '/private_v1/photo/1/'
        put_data = {
            'caption': 'awesome'
        }
        resp = self.api_client.put(uri, data=put_data, format='json', authentication=self.get_credentials('PUT', uri))
        data = self.deserialize(resp)

        # make sure the resource has a valid response
        self.assertHttpOK(resp)

        # test to make sure all the keys are in the response
        self.assertEqual(data['caption'], put_data['caption'])

    def test_delete_photo(self):
        uri = '/private_v1/photo/1/'
        resp = self.api_client.delete(uri, format='json', authentication=self.get_credentials('DELETE', uri))

        self.assertHttpAccepted(resp)
