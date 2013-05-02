# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth.db_v1 import DatabaseAuthentication
from api.models import ApiAccount
from data.models import Event

class Partner_v1__EventResourceTest(ResourceTestCase):
    fixtures = ['api_accounts_and_keys.json', 'packages.json', 'accounts_and_users.json', 'events.json']

    def setUp(self):
        super(Partner_v1__EventResourceTest, self).setUp()
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        self.api_account_1 = ApiAccount.objects.get()
        self.events = Event.objects.filter(account__api_account=self.api_account_1)
        self.event_1 = self.events[0]

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_events(self):
        uri = '/partner_v1/event/'
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # make sure we have the right number of accounts
        self.assertEqual(len(self.deserialize(resp)['objects']), self.events.count())

    def test_get_event(self):
        uri = '/partner_v1/event/{0}/'.format(self.event_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'account',
            'created',
            'enabled',
            'end',
            'locations',
            'photo_count',
            'pin',
            'public',
            'resource_uri',
            'start',
            'title',
            'tz_offset',
            'url',
        ])
