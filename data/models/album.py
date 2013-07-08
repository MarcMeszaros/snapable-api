from django.db import models

from data.models import Event
from data.models import Photo

class Album(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    event = models.ForeignKey(Event)
    photo = models.ForeignKey(Photo, null=True, default=None, on_delete=models.SET_NULL)

    short_name = models.CharField(max_length=255, help_text='The albums short name.')
    name = models.CharField(max_length=255, help_text='The album name.')
    description = models.TextField(help_text='A description of the album.')
    creation_date = models.DateTimeField(auto_now_add=True, help_text='When the album was created. (UTC)')