# python
import time

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

        # Fetch the objects we'll use in testing.
        # Note that we aren't using PKs because they can change depending
        # on what other tests are running.
        self.event_1 = Event.objects.all()[0]

        self.post_data = {
            'account': '/private_v1/account/3/', # account 3 has no users
            'end': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() + 60*60)),
            'start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'title': 'My awesome test event',
            'url': 'awesome-test-event',
            'tz_offset': 0,
        }

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

    def test_get_events_search(self):
        uri_post = '/private_v1/event/'
        uri_get = '/private_v1/event/search/'
        data_get = {'q': 'test', 'enabled': 'true', 'order_by': 'end'}

        resp_post = self.api_client.post(uri_post, data=self.post_data, format='json', authentication=self.get_credentials('POST', uri_post))

        # make sure the resource was created
        self.assertHttpCreated(resp_post)

        resp_get = self.api_client.get(uri_get, data=data_get, format='json', authentication=self.get_credentials('GET', uri_get))

        # make sure the response is valid
        self.assertValidJSONResponse(resp_get)
        # make sure we have some search results
        self.assertTrue(self.deserialize(resp_get)['meta']['total_count'] > 0)
