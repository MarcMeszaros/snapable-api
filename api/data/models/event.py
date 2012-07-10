from django.db import models
from api.data.models.user import User
from api.data.models.package import Package

class Event(models.Model):
    
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
    access_count = models.IntegerField()
    enabled = models.BooleanField()