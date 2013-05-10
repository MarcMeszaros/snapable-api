# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth.db_v1 import DatabaseAuthentication
from api.models import ApiAccount
from data.models import Guest

class Partner_v1__GuestResourceTest(ResourceTestCase):
    fixtures = ['api_accounts_and_keys.json', 'packages.json', 'accounts_and_users.json', 'events.json', 'guests.json']

    def setUp(self):
        super(Partner_v1__GuestResourceTest, self).setUp()
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        self.api_account_1 = ApiAccount.objects.all()[0]
        self.guests = Guest.objects.filter(event__account__api_account=self.api_account_1)
        self.guest_1 = self.guests[0]

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_guests(self):
        uri = '/partner_v1/guest/'
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # make sure we have the right number of accounts
        self.assertEqual(len(self.deserialize(resp)['objects']), self.guests.count())

    def test_get_event(self):
        uri = '/partner_v1/guest/{0}/'.format(self.guest_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'email',
            'event',
            'name',
            'resource_uri',
        ])
