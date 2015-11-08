# django
from django.test import TestCase

# snapable
from data.models import PasswordNonce

class PhotoTestCase(TestCase):

    def setUp(self):
        """Setup the necessary objects for testing."""
        pass

    def test_random_sha512(self):
        """Test to make sure random SHA512's are generated."""
        first_sha512 = PasswordNonce.random_sha512()
        second_sha512 = PasswordNonce.random_sha512()

        # make sure the digest is the right length
        self.assertEqual(len(first_sha512), 128)
        self.assertEqual(len(second_sha512), 128)

        # make sure the hashes are not equivalent
        self.assertNotEqual(first_sha512, second_sha512)
