from django.db import models
from jsonfield import JSONField

class Package(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'
    
    short_name = models.CharField(max_length=255, help_text='The package short name.')
    name = models.CharField(max_length=255, help_text='The package long name.')
    price = models.IntegerField(help_text='The package price. (CENTS)')
    enabled = models.BooleanField(help_text='If the package is enabled.')
    items = JSONField(help_text='The items included in the package.')