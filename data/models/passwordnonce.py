# python
import hashlib
import random

# django/tastypie
from django.db import models

class PasswordNonce(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    # the model fields
    user = models.ForeignKey('User')

    nonce = models.CharField(max_length=255, unique=True, help_text="The password nonce.")
    is_valid = models.BooleanField(default=True, help_text='If the nonce is still valid.')
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the nonce was created. (UTC)')

    def __unicode__(self):
        return str({
            'created_at': self.created_at,
            'nonce': self.nonce,
            'is_valid': self.is_valid,
        })

    def save(self, *args, **kwargs):
        """
        Override the default Django model save function and make sure a nonce
        is set and unique.
        """
        if (len(self.nonce) <= 0):
            nonce = PasswordNonce.random_sha512()
            while (PasswordNonce.objects.filter(nonce=nonce).count() > 0):
                nonce = PasswordNonce.random_sha512()
            self.nonce = nonce

        super(PasswordNonce, self).save(*args, **kwargs) # Call the "real" save() method.

    @staticmethod
    def random_sha512():
        """
        Generate a random sha512 hash
        """
        return hashlib.sha512(str(random.SystemRandom().getrandbits(512))).hexdigest()
