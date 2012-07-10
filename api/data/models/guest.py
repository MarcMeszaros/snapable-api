from django.db import models
from api.data.models.event import Event
from api.data.models.type import Type

class Guest(models.Model):
    
    class Meta:
        app_label = 'data'

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    start = models.DateTimeField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)