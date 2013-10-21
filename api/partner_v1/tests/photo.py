# python
import os

# django/tastypie
from django.conf import settings
from tastypie.test import ResourceTestCase, TestApiClient

# snapable
from api.auth.db_v1 import DatabaseAuthentication
from api.models import ApiAccount
from api.utils.serializers import MultipartSerializer
from data.models import Event, Photo

class Partner_v1__PhotoResourceTest(ResourceTestCase):
    fixtures = ['api_accounts_and_keys.json', 'packages.json', 'accounts_and_users.json', 'events.json', 'guests.json', 'photos.json']

    def setUp(self):
        super(Partner_v1__PhotoResourceTest, self).setUp()
        # we need a custom serializer for multipart uploads
        self.api_client = TestApiClient(serializer=MultipartSerializer())
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        self.api_account_1 = ApiAccount.objects.all()[0]
        self.events = Event.objects.filter(account__api_account=self.api_account_1)
        self.photos = Photo.objects.filter(event__account__api_account=self.api_account_1)
        self.photo_1 = self.photos[0]

        # The data we'll send on POST requests
        filename = 'trashcat.jpg'
        filepath = os.path.join(settings.PROJECT_PATH, 'api', 'assets', filename)
        f = open(filepath, 'rb')

        self.post_data = {
            'event': '/partner_v1/event/{0}/'.format(self.events[0].pk),
            'caption': 'My super awesome caption!',
            'image': {
                'filename': filename,
                'data': f.read(),
            }
        }

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_photos(self):
        uri = '/partner_v1/photo/'
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # make sure we have the right number of objects
        self.assertNotEqual(Photo.objects.all().count(), self.photos.count())
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], self.photos.count())

    def test_get_photo(self):
        uri = '/partner_v1/photo/{0}/'.format(self.photo_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'caption',
            'created_at',
            'event',
            'guest',
            'resource_uri',
        ])

    def test_post_photo(self):
        uri = '/partner_v1/photo/'
        resp = self.api_client.post(uri, data=self.post_data, format='multipart', authentication=self.get_credentials('POST', uri))

        # make sure the resource was created
        self.assertHttpCreated(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'caption',
            'created_at',
            'event',
            'guest',
            'resource_uri',
        ])
