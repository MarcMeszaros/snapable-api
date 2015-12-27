# django
from django.test import TestCase

# snapable
from data.models import Order

class OrderTestCase(TestCase):
    fixtures = ['accounts_and_users.json', 'orders.json']

    def setUp(self):
        """Setup the necessary objects for testing."""
        pass

    def test_calculate(self):
        o = Order.objects.get(pk=1)
        o.calculate()

        self.assertEquals(o.amount, 7900)
