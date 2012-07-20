from django.db import models

from data.models import Package
from data.models import User

class Event(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'
    
    user = models.ForeignKey(User)
    package = models.ForeignKey(Package)
    start = models.DateTimeField()
    end = models.DateTimeField()
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    pin = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_access = models.DateTimeField(auto_now_add=True)
    access_count = models.IntegerField(default=0)
    enabled = models.BooleanField()