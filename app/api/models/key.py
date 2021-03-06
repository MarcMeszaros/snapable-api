# python
import hashlib
import uuid

# django/tastypie/libs
from bitfield import BitField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# snapable
import utils.redis


@python_2_unicode_compatible
class ApiKey(models.Model):

    # the choices for the interval field
    API_PARTNER_V1 = 'partner_v1'
    API_PRIVATE_V1 = 'private_v1'
    API_CHOICES = (
        (API_PARTNER_V1, 'Partner (v1)'),
        (API_PRIVATE_V1, 'Private (v1)'),
    )

    # relations
    account = models.ForeignKey('ApiAccount')

    # regular fields
    key = models.CharField(max_length=255, unique=True, db_index=True, help_text='The API key.')
    secret = models.CharField(max_length=255, help_text='The API key secret.')
    version = models.CharField(max_length=25, choices=API_CHOICES, help_text='The API version that the key has access to.')
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the API key was created. (UTC)')
    is_enabled = models.BooleanField(default=True, help_text='If the API key is enabled.')

    # permission mask flags
    permission_mask = BitField(flags=(
        ('create', 'Create'),
        ('read', 'Read'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ),
    default=['create', 'read', 'update', 'delete'],
    help_text='What permissions this API key has on data in the system.')

    def __str__(self):
        return '{0} ({1})'.format(self.key, self.account.company)

    def __repr__(self):
        return str({
            'account': self.account,
            'created_at': self.created_at,
            'is_enabled': self.is_enabled,
            'key': self.key,
            'pk': self.pk,
            'secret': self.secret,
            'version': self.version,
        })

    def save(self, *args, **kwargs):
        if not self.key:
            key = ApiKey.generate_key()  # generate a key
            # in the event the key already exists, keep trying new ones
            while (ApiKey.objects.filter(key=key).count() > 0):
                key = ApiKey.generate_key()
            self.key = key  # set the key in the model
        if not self.secret:
            self.secret = ApiKey.generate_secret()

        utils.redis.client.delete('api_key_{0}'.format(self.key))  # delete any cache
        return super(ApiKey, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return hashlib.md5(uuid.uuid4().hex).hexdigest()

    @staticmethod
    def generate_secret():
        return hashlib.sha256(uuid.uuid4().hex).hexdigest()
