# python
import time

# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth.db_v1 import DatabaseAuthentication
from api.models import ApiAccount
from data.models import Account, Event

class Partner_v1__EventResourceTest(ResourceTestCase):
    fixtures = ['api_accounts_and_keys.json', 'packages.json', 'accounts_and_users.json', 'events.json']

    def setUp(self):
        super(Partner_v1__EventResourceTest, self).setUp()
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        self.api_account_1 = ApiAccount.objects.all()[0]
        self.accounts = self.api_account_1.account_set.all()
        self.events = Event.objects.filter(account__api_account=self.api_account_1)
        self.event_1 = self.events[0]

        self.post_data = {
            'account': '/partner_v1/account/{0}/'.format(self.accounts[0].pk),
            'end': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() + 60*60)),
            'start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'title': 'Super Awesome Title',
            'url': 'super-awesome-title',
        }

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

    def test_post_event(self):
        uri = '/partner_v1/event/'
        self.assertEqual(self.accounts[0].event_set.count(), 1) # make sure there is one event
        resp = self.api_client.post(uri, data=self.post_data, format='json', authentication=self.get_credentials('POST', uri))

        # make sure it was not created
        self.assertHttpCreated(resp)
        self.assertEqual(self.accounts[0].event_set.count(), 2)

    def test_post_event_invalid_url(self):
        uri = '/partner_v1/event/'
        new_event = self.post_data.copy()
        new_event['url'] = Event.objects.all()[0].url # get an existing url
        
        # existing url should fail
        resp = self.api_client.post(uri, data=new_event, format='json', authentication=self.get_credentials('POST', uri))
        self.assertHttpBadRequest(resp)

        # invalid urls should fail
        new_event2 = self.post_data.copy()
        new_event2['url'] = 'inva&lid-url'
        resp = self.api_client.post(uri, data=new_event2, format='json', authentication=self.get_credentials('POST', uri))
        self.assertHttpBadRequest(resp)

        new_event2['url'] = 'inva#lid-url'
        resp = self.api_client.post(uri, data=new_event2, format='json', authentication=self.get_credentials('POST', uri))
        self.assertHttpBadRequest(resp)

        new_event2['url'] = 'invalid-url '
        resp = self.api_client.post(uri, data=new_event2, format='json', authentication=self.get_credentials('POST', uri))
        self.assertHttpBadRequest(resp)
