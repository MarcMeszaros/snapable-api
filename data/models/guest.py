# django/tastypie/libs
from django.db import models

# snapable
from data.models import Event

class Guest(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, help_text='The guest name.')
    email = models.CharField(max_length=255, help_text='The guest email address.')
    invited = models.BooleanField(default=False, help_text='If the guest has been invited.')
    created_at = models.DateTimeField(auto_now_add=True, help_text='The guest timestamp.')

    # virtual properties #
    # return the number of photos related to this event
    def _get_photo_count(self):
        return self.photo_set.count()

    def _set_photo_count(self, value):
        pass

    # create the property
    photo_count = property(_get_photo_count, _set_photo_count)

    def __unicode__(self):
        return str({
            'created_at': self.created_at,
            'email': self.email,
            'event': self.event,
            'invited': self.invited,
            'name': self.name,
            'photo_count': self.photo_count,
        })