# -*- coding: utf-8 -*-
from __future__ import absolute_import

# django/tastypie
from tastypie.test import ResourceTestCase

# snapable
from api.auth import DatabaseAuthentication


class Private_v1__OrderResourceTest(ResourceTestCase):
    fixtures = ['packages.json', 'api_accounts_and_keys.json', 'accounts_and_users.json', 'events.json', 'photos.json', 'orders.json']

    def setUp(self):
        super(Private_v1__OrderResourceTest, self).setUp()
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

        self.post_account = {
            'email': 'marc+test@snapable.com',
            'password': 'monkey123',
            'first_name': 'Bob',
            'last_name': 'Example',
            'items': {
                'package': 2,
                'account_addons': [],
                'event_addons': [],
            },
            'title': 'New Event Title',
            'url': 'new-event-title',
            'start': '2014-02-16T12:34:12Z',
            'end': '2014-02-17T12:34:12Z',
            'tz_offset': -300,
            'address': '1 Infinite Loop',
            'lat': '0.000000',
            'lng': '0.000000',
        }

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_post_order(self):
        uri = '/private_v1/order/'
        resp = self.api_client.post(uri, data=self.post_data_1, format='json', authentication=self.get_credentials('POST', uri))
        data = self.deserialize(resp)

        # make sure the resource was created
        self.assertHttpCreated(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(data, [
            'account',
            'amount',
            'amount_refunded',
            'charge_id',
            'coupon',
            'created_at',
            'items',
            'is_paid',
            'paid',
            'payment_gateway_invoice_id',
            'price',
            'resource_uri',
            'total_price',
            'user',
        ])

        # make sure the ammount is correct
        self.assertEqual(data['amount'], self.post_data_1['total_price'])

    def test_post_order_account(self):
        uri = '/private_v1/order/account/'
        resp = self.api_client.post(uri, data=self.post_account, format='json', authentication=self.get_credentials('POST', uri))

        # make sure the resource was created
        self.assertHttpCreated(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'account',
            'address',
            'amount',
            'amount_refunded',
            'charge_id',
            'coupon',
            'created_at',
            'email',
            'end',
            'event',
            'first_name',
            'items',
            'is_paid',
            'last_name',
            'lat',
            'lng',
            'paid',
            'password',
            'price',
            'resource_uri',
            'start',
            'title',
            'tz_offset',
            'url',
            'user',
        ])

    def test_delete_order(self):
        uri = '/private_v1/order/1/'
        resp = self.api_client.delete(uri, format='json', authentication=self.get_credentials('DELETE', uri))

        self.assertHttpMethodNotAllowed(resp)
