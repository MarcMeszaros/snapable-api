import unittest

from data.models import Account
from data.models import Event
from data.models import Package
from data.models import Photo
from data.models import Type

class PhotoTestCase(unittest.TestCase):

    def setUp(self):
        """Setup the necessary objects for testing."""
        self.account = Account.objects.create(package=Package.objects.get(pk=1))
        self.event = Event.objects.create(account=self.account, start='2012-01-01 12:45:00+00:00', end='2012-01-01 12:45:12+00:00')
        self.photo1 = Photo.objects.create(event=self.event, type=Type.objects.get(pk=5))
        self.photo2 = Photo.objects.create(event=self.event, type=Type.objects.get(pk=5))

    def testBasic(self):
        """Basic test."""
        self.assertEqual(self.photo1.type, Type.objects.get(pk=5))