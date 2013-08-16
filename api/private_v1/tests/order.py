# python
import os
import re

# django/tastypie
from django.conf import settings
from tastypie.test import ResourceTestCase

# snapable
from api.auth.server import ServerAuthentication

class Private_v1__OrderResourceTest(ResourceTestCase):
    fixtures = ['packages.json', 'accounts_and_users.json', 'events.json', 'photos.json', 'orders.json']

    def setUp(self):
        super(Private_v1__OrderResourceTest, self).setUp()
        # we need a custom serializer for multipart uploads
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        self.post_data_1 = {
            'total_price': 7900,
            'account': '/private_v1/account/1/',
            'user': '/private_v1/user/1/',
            'items': {
                'package': 2,
                'account_addons': [],
                'event_addons': [],
            },
            'paid': True,
            'payment_gateway_invoice_id': 'ch_1YXHVcBds4VRFX',
        }

    def get_credentials(self, method, uri):
        return ServerAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_post_order(self):
        uri = '/private_v1/order/'
        resp = self.api_client.post(uri, data=self.post_data_1, format='json', authentication=self.get_credentials('POST', uri))
        data = self.deserialize(resp)

        # make sure the resource was created
        self.assertHttpCreated(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'account',
            'amount',
            'amount_refunded',
            'charge_id',
            'coupon',
            'items',
            'paid',
            'payment_gateway_invoice_id',
            'price',
            'resource_uri',
            'timestamp',
            'total_price',
            'user',
        ])

        # make sure the ammount is correct
        self.assertEqual(data['amount'], self.post_data_1['total_price'])

    def test_delete_order(self):
        uri = '/private_v1/order/1/'
        resp = self.api_client.delete(uri, format='json', authentication=self.get_credentials('DELETE', uri))

        self.assertHttpMethodNotAllowed(resp)
