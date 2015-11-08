# python
import time

# django/tastypie/libs
from tastypie.test import ResourceTestCase, TestApiClient

# snapable
from api.auth import DatabaseAuthentication
from api.utils.serializers import SnapSerializer
from data.models import Event

class Private_v1__EventResourceTest(ResourceTestCase):
    fixtures = ['packages.json', 'api_accounts_and_keys.json', 'accounts_and_users.json', 'events.json', 'photos.json']

    def setUp(self):
        super(Private_v1__EventResourceTest, self).setUp()
        # we need a custom serializer for multipart uploads
        self.api_client = TestApiClient(serializer=SnapSerializer())
        self.api_key = 'key123'
        self.api_secret = 'sec123'

        # Fetch the objects we'll use in testing.
        # Note that we aren't using PKs because they can change depending
        # on what other tests are running.
        self.event_1 = Event.objects.all()[0]

        self.post_data = {
            'account': '/private_v1/account/3/', # account 3 has no users
            'end': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() + 60*60)),
            'start': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'title': 'My awesome test event',
            'url': 'awesome-test-event',
            'tz_offset': 0,
        }

        self.old_date_data = {
            'are_photos_streamable': True,
            'end': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() + 60*60)),
            'is_public': False,
            'start': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            'title': 'Wedding Republic & Snapable Office Party',
            'url': 'wr-snap-party',
        }

        self.patch_data = {
            'are_photos_streamable': True,
            'end_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() + 60*60)),
            'is_public': False,
            'start_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'title': 'Wedding Republic & Snapable Office Party',
            'url': 'wr-snap-party',
        }

    def get_credentials(self, method, uri):
        return DatabaseAuthentication.create_signature(self.api_key, self.api_secret, method, uri)

    def test_get_event(self):
        uri = '/private_v1/event/{0}/'.format(self.event_1.pk)
        resp = self.api_client.get(uri, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource was created
        self.assertValidJSONResponse(resp)

        # test to make sure all the keys are in the response
        self.assertKeys(self.deserialize(resp), [
            'account',
            'addons',
            'addresses',
            'are_photos_streamable',
            'cover',
            'created',
            'created_at',
            'creation_date',
            'enabled',
            'end',
            'end_at',
            'is_enabled',
            'is_public',
            'package',
            'photo_count',
            'pin',
            'public',
            'resource_uri',
            'start',
            'start_at',
            'title',
            'type',
            'tz_offset',
            'url',
            'user',
            'uuid'
        ])

    def test_get_events(self):
        uri = '/private_v1/event/'
        data_get = {'start_at__gte': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - 60))}
        resp = self.api_client.get(uri, data=data_get, format='json', authentication=self.get_credentials('GET', uri))

        # make sure the resource was created
        self.assertValidJSONResponse(resp)

        count = self.deserialize(resp)['meta']['total_count']
        self.assertTrue(count >= 0)
        self.assertTrue(count < Event.objects.count())

    def test_get_event_cover(self):
        # this event doesn't have any data in cloud files
        uri = '/private_v1/event/{0}/'.format(self.event_1.pk)
        resp = self.api_client.get(uri, format='jpeg', authentication=self.get_credentials('GET', uri))

        self.assertHttpNotFound(resp)

    def test_get_events_search(self):
        uri_post = '/private_v1/event/'
        uri_get = '/private_v1/event/search/'
        data_get = {'q': 'event', 'enabled': 'true', 'order_by': 'end'}
        events = Event.objects.all()
        events_count = events.count() # count() checks database, not queryset, so we save now

        resp_post = self.api_client.post(uri_post, data=self.post_data, format='json', authentication=self.get_credentials('POST', uri_post))

        # make sure the resource was created
        self.assertHttpCreated(resp_post)

        resp_get = self.api_client.get(uri_get, data=data_get, format='json', authentication=self.get_credentials('GET', uri_get))

        # make sure the response is valid
        self.assertValidJSONResponse(resp_get)
        # make sure we have some search results
        self.assertTrue(self.deserialize(resp_get)['meta']['total_count'] > 0)

        # we should have n+1 where n is existing events (+ 1 new)
        self.assertEqual(self.deserialize(resp_get)['meta']['total_count'], events_count + 1)

        # the first should be the new event url
        self.assertEqual(self.deserialize(resp_get)['objects'][0]['url'], self.post_data['url'])

        # the second should be the first event url
        self.assertEqual(self.deserialize(resp_get)['objects'][1]['url'], self.event_1.url)

    def test_put_event(self):
        uri_put = '/private_v1/event/{0}/'.format(self.event_1.pk)
        resp = self.api_client.put(uri_put, data=self.patch_data, format='json', authentication=self.get_credentials('PUT', uri_put))

        event = Event.objects.get(pk=self.event_1.pk)
        event_start = event.start_at.strftime('%Y-%m-%dT%H:%M:%SZ')

        self.assertEqual(event_start, self.patch_data['start_at'])

        # deprecated code test
        resp = self.api_client.put(uri_put, data=self.old_date_data, format='json', authentication=self.get_credentials('PUT', uri_put))

        event = Event.objects.get(pk=self.event_1.pk)
        event_start = event.start_at.strftime('%Y-%m-%d %H:%M:%S')

        self.assertEqual(event_start, self.old_date_data['start'])

    def test_patch_event(self):
        uri_patch = '/private_v1/event/{0}/'.format(self.event_1.pk)
        resp = self.api_client.patch(uri_patch, data=self.patch_data, format='json', authentication=self.get_credentials('PATCH', uri_patch))

        event = Event.objects.get(pk=self.event_1.pk)
        event_start = event.start_at.strftime('%Y-%m-%dT%H:%M:%SZ')

        self.assertEqual(event_start, self.patch_data['start_at'])

        # deprecated code test
        resp = self.api_client.patch(uri_patch, data=self.old_date_data, format='json', authentication=self.get_credentials('PATCH', uri_patch))

        event = Event.objects.get(pk=self.event_1.pk)
        event_start = event.start_at.strftime('%Y-%m-%d %H:%M:%S')

        self.assertEqual(event_start, self.old_date_data['start'])
