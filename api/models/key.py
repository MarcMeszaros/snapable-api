import hashlib
import uuid

from django.db import models

from api.models import ApiAccount

class ApiKey(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'api'

    # relations
    account = models.ForeignKey(ApiAccount)

    # regular fields
    key = models.CharField(max_length=255, unique=True, db_index=True, help_text='The api key.')
    secret = models.CharField(max_length=255, help_text='The api key secret.')
    version = models.CharField(max_length=25, help_text='The api version that the key has access to.')
    created = models.DateTimeField(auto_now_add=True, help_text='When the api key was created. (UTC)')
    enabled = models.BooleanField(default=True, help_text='If the api key is enabled.')

    def __unicode__(self):
        return str({
            'api_account': self.api_account,
            'key': self.key, 
            'secret': self.secret,
            'version': self.version,
            'created': self.created,
            'enabled': self.enabled,
        })

    def save(self, *args, **kwargs):
        if not self.key:
            key = ApiKey.generate_key() # generate a key
            # in the event the key already exists, keep trying new ones
            while (ApiKey.objects.filter(key=key).count() > 0):
                key = ApiKey.generate_key()
            self.key = key # set the key in the model
        if not self.secret:
            self.secret = ApiKey.generate_secret()
            
        return super(ApiKey, self).save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return hashlib.md5(uuid.uuid4().hex).hexdigest()

    @staticmethod
    def generate_secret():
        return hashlib.sha256(uuid.uuid4().hex).hexdigest()