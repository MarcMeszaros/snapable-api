# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth import DatabaseAuthentication
from data.models import Location

class Private_v1__AddressResourceTest(ResourceTestCase):
    fixtures = ['packages.json', 'api_accounts_and_keys.json', 'accounts_and_users.json', 'events.json', 'guests.json']

    def setUp(self):
        super(Private_v1__AddressResourceTest, self).setUp()
        # we need a custom serializer for multipart uploads
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        self.addresses = Location.objects.all()
        self.address_1 = self.addresses[0]

        # The data we'll send on POST requests
        self.post_data = {
            'address': '126 York Street, Suite 200, Ottawa, ON',
            'event': '/private_v1/event/1/',
            'lat': '45.429265',
            'lng': '-75.69005',
        }

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_addresses(self):
        uri = '/private_v1/address/'
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # make sure we have the right number of objects
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], self.addresses.count())

    def test_get_address(self):
        uri = '/private_v1/address/{0}/'.format(self.address_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'address',
            'event',
            'lat',
            'lng',
            'resource_uri',
        ])
