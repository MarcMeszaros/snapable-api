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
    guest = models.ForeignKey(Guest, null=True, default=None, on_delete=models.SET_NULL)
    type = models.ForeignKey(Type)

    caption = models.CharField(max_length=255, help_text='The photo caption.')
    streamable = models.BooleanField(help_text='If the photo is streamable.')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='The photo timestamp.')
    metrics = models.TextField(help_text='JSON metrics about the photo.') # JSON metrics