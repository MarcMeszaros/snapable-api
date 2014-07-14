# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth import DatabaseAuthentication
from api.models import ApiAccount
from data.models import Event, Location

class Partner_v1__LocationResourceTest(ResourceTestCase):
    fixtures = ['api_accounts_and_keys.json', 'packages.json', 'accounts_and_users.json', 'events.json', 'guests.json']

    def setUp(self):
        super(Partner_v1__LocationResourceTest, self).setUp()
        self.api_key = 'key123_partner'
        self.api_secret = 'sec123_partner'

        self.api_account_1 = ApiAccount.objects.all()[0]
        self.events = Event.objects.filter(account__api_account=self.api_account_1)
        self.locations = Location.objects.filter(event__account__api_account=self.api_account_1)
        self.location_1 = self.locations[0]

        self.post_data = {
            'event': '/partner_v1/event/{0}/'.format(self.events[0].pk),
            'address': '123 My Address St., SomeTown, Province, Country',
            'lat': '123.000000',
            'lng': '90.000000',
        }

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_locations(self):
        uri = '/partner_v1/location/'
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # make sure we have the right number of objects
        self.assertNotEqual(Location.objects.all().count(), self.locations.count())
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], self.locations.count())

    def test_get_location(self):
        uri = '/partner_v1/location/{0}/'.format(self.location_1.pk)
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

    def test_post_location(self):
        uri = '/partner_v1/location/'
        self.assertEqual(self.events[0].location_set.count(), 1)
        resp = self.api_client.post(uri, data=self.post_data, format='json', authentication=self.get_credentials('POST', uri))

        # make sure the we can't add more than one location
        self.assertHttpCreated(resp)
        self.assertEqual(self.events[0].location_set.count(), 2)

        self.assertNotEqual(Location.objects.all().count(), self.locations.count())
