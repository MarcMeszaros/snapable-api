# django/tastypie/libs
from tastypie.test import ResourceTestCase

# snapable
from api.auth.server import ServerAuthentication
from data.models import Event

class Private_v1__EventResourceTest(ResourceTestCase):
    fixtures = ['packages.json', 'accounts_and_users.json', 'events.json', 'photos.json']

    def setUp(self):
        super(Private_v1__EventResourceTest, self).setUp()
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        # Fetch the ``Event`` object we'll use in testing.
        # Note that we aren't using PKs because they can change depending
        # on what other tests are running.
        self.event_1 = Event.objects.get()

    def get_credentials(self, method, uri):
        return ServerAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_event(self):
        uri = '/private_v1/event/{0}/'.format(self.event_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource was created
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'account',
            'addons',
            'addresses',
            'cover',
            'created',
            'creation_date',
            'enabled',
            'end',
            'package',
            'photo_count',
            'pin',
            'public',
            'resource_uri',
            'start',
            'title',
            'type',
            'tz_offset',
            'url',
            'user',
        ])
