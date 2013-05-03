# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth.server import ServerAuthentication
from data.models import User

class Private_v1__UserResourceTest(ResourceTestCase):
    fixtures = ['packages.json', 'accounts_and_users.json', 'events.json', 'guests.json']

    def setUp(self):
        super(Private_v1__UserResourceTest, self).setUp()
        # we need a custom serializer for multipart uploads
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        self.users = User.objects.all()
        self.user_1 = self.users[0]

        # The data we'll send on POST requests
        self.post_data = {
            'billing_zip': '00000',
            'email': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'terms': True,
        }

    def get_credentials(self, method, uri):
        return ServerAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_users(self):
        uri = '/private_v1/user/'
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # make sure we have the right number of objects
        self.assertEqual(self.deserialize(resp)['meta']['total_count'], self.users.count())

    def test_get_user(self):
        uri = '/private_v1/user/{0}/'.format(self.user_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource is valid
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'accounts',
            'billing_zip',
            'creation_date',
            'email',
            'first_name',
            'last_name',
            'password_algorithm',
            'password_iterations',
            'password_salt',
            'resource_uri',
            'terms',
        ])

    def test_post_user(self):
        uri = '/private_v1/user/'
        resp = self.api_client.post(uri, data=self.post_data, format='json', authentication=self.get_credentials('POST', uri))

        # make sure the resource was created
        self.assertHttpCreated(resp)
        
        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'accounts',
            'billing_zip',
            'creation_date',
            'email',
            'first_name',
            'last_name',
            'resource_uri',
            'terms',
        ])
