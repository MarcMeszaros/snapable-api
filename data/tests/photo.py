from django.test import TestCase

from data.models import Account
from data.models import Event
from data.models import Photo

class PhotoTestCase(TestCase):
    fixtures = ['packages.json', 'accounts_and_users.json', 'events.json']

    def setUp(self):
        """Setup the necessary objects for testing."""
        self.event = Event.objects.get(pk=1)

    def testExists(self):
        """Test to make sure all the objects from fixtures and setUp() exist."""
        self.assertNotEqual(Account.objects.get(pk=1), None)
        self.assertNotEqual(Event.objects.get(pk=1), None)

    def testCreatePhoto(self):
        """Test to make sure photo is properly created."""
        self.photo1 = Photo.objects.create(event=self.event)