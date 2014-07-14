# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth.db_v1 import DatabaseAuthentication
from api.models import ApiAccount
from data.models import Account

class Partner_v1__AccountResourceTest(ResourceTestCase):
    fixtures = ['api_accounts_and_keys.json', 'packages.json', 'accounts_and_users.json']

    def setUp(self):
        super(Partner_v1__AccountResourceTest, self).setUp()
        self.api_key = 'key123_partner'
        self.api_secret = 'sec123_partner'

        self.api_account_1 = ApiAccount.objects.all()[0]
        self.accounts = Account.objects.filter(api_account=self.api_account_1)
        self.account_1 = self.accounts[0]

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_accounts(self):
        uri = '/partner_v1/account/'
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # make sure we have the right number of accounts
        self.assertEqual(len(self.deserialize(resp)['objects']), self.accounts.count())

    def test_get_account(self):
        uri = '/partner_v1/account/{0}/'.format(self.account_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'resource_uri',
            'users',
        ])
