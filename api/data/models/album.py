from django.db import models
from api.data.models.event import Event
from api.data.models.type import Type

class Album(models.Model):
    
    class Meta:
        app_label = 'data'

    event = models.ForeignKey(Event)
    type = models.ForeignKey(Type)
    short_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)