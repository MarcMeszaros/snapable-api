from django.db import models

from data.models import Event
from data.models import Guest
from data.models import Type

class Photo(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    # the model fields
    event = models.ForeignKey(Event)
    guest = models.ForeignKey(Guest)
    type = models.ForeignKey(Type)
    filename = models.CharField(max_length=255, unique=True)
    caption = models.CharField(max_length=255)
    streamable = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metrics = models.TextField() # JSON metrics