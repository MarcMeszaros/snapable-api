from django.db import models

from data.models import Event
from data.models import Type

class Guest(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, help_text='The guest name.')
    email = models.CharField(max_length=255, help_text='The guest email address.')

    def __unicode__(self):
        return str({
            'email': self.email,
            'event': self.event,
            'name': self.name,
            'type': self.type,
        })