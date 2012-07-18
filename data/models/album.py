from django.db import models

from data.models import Event
from data.models import Photo
from data.models import Type

class Album(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    event = models.ForeignKey(Event)
    type = models.ForeignKey(Type)
    photo = models.ForeignKey(Photo, null=True, default=None, on_delete=models.SET_NULL)
    short_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)