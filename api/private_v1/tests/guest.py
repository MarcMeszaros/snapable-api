# django/tastypie/libs
from tastypie.test import ResourceTestCase

# snapable
from api.auth.server import ServerAuthentication
from data.models import Guest

class Private_v1__GuestResourceTest(ResourceTestCase):
    fixtures = ['packages.json', 'accounts_and_users.json', 'events.json', 'photos.json', 'guests.json']

    def setUp(self):
        super(Private_v1__GuestResourceTest, self).setUp()
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        # Fetch the ``Guest`` object we'll use in testing.
        # Note that we aren't using PKs because they can change depending
        # on what other tests are running.
        self.guest_1 = Guest.objects.get()

        self.post_data = {
            'event': '/private_v1/event/1/',
            'type': '/private_v1/type/1/',
        }

    def get_credentials(self, method, uri):
        return ServerAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_guest(self):
        uri = '/private_v1/guest/{0}/'.format(self.guest_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource was created
        self.assertValidJSONResponse(resp)
        
        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'email',
            'event',
            'invited',
            'name',
            'resource_uri',
            'type',
        ])

        self.assertEqual(self.deserialize(resp)['type'], '/private_v1/type/6/')

    def test_post_guest(self):
        uri = '/private_v1/guest/'
        resp = self.api_client.post(uri, data=self.post_data, format='json', authentication=self.get_credentials('POST', uri))
        data = self.deserialize(resp)

        # make sure the resource was created
        self.assertHttpCreated(resp)
        
        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'email',
            'event',
            'invited',
            'name',
            'resource_uri',
            'type',
        ])
