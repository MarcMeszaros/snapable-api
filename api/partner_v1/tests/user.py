# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth.db_v1 import DatabaseAuthentication
from api.models import ApiAccount
from data.models import User

class Partner_v1__UserResourceTest(ResourceTestCase):
    fixtures = ['api_accounts_and_keys.json', 'packages.json', 'accounts_and_users.json', 'events.json', 'guests.json']

    def setUp(self):
        super(Partner_v1__UserResourceTest, self).setUp()
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        self.api_account_1 = ApiAccount.objects.all()[0]
        self.users = User.objects.filter(account__api_account=self.api_account_1)
        self.user_1 = self.users[0]

        self.post_data = {
            'email': 'bob+testexample3@example.com',
            'first_name': 'Bob', 
            'last_name': 'Example3',
        }

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_users(self):
        uri = '/partner_v1/user/'
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # make sure we have the right number of objects
        self.assertEqual(len(self.deserialize(resp)['objects']), self.users.count())

    def test_get_user(self):
        uri = '/partner_v1/user/{0}/'.format(self.user_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'accounts',
            'email',
            'first_name',
            'last_name',
            'resource_uri',
        ])

    def test_update_user(self):
        uri = '/partner_v1/user/{0}/'.format(self.user_1.pk)
        update_data = {
            'email': 'bob.test@example.com',
        }
        resp = self.api_client.put(uri, data=update_data, format='json', authentication=self.get_credentials('PUT', uri))

        # make sure it was updated
        self.assertHttpOK(resp)

        # check the email value
        self.assertEqual(self.deserialize(resp)['email'], 'bob.test@example.com')

    def test_post_user(self):
        uri = '/partner_v1/user/'
        resp = self.api_client.post(uri, data=self.post_data, format='json', authentication=self.get_credentials('POST', uri))

        # make sure it was create
        self.assertHttpCreated(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'accounts',
            'email',
            'first_name',
            'last_name',
            'resource_uri',
        ])

        # check the email value
        self.assertEqual(self.deserialize(resp)['email'], 'bob+testexample3@example.com')
