from django.db import models

from data.models import Event

class Address(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    event = models.ForeignKey(Event)

    address = models.CharField(max_length=255, help_text='The event address.')
    lat = models.DecimalField(max_digits=9, decimal_places=6, help_text='The address latitude.') # +/- 180.123456, accuracy: 0.111 m (ie. 11.1cm)
    lng = models.DecimalField(max_digits=9, decimal_places=6, help_text='The address longitude.') # +/- 180.123456, accuracy: 0.111 m (ie. 11.1cm)
    creation_date = models.DateTimeField(auto_now_add=True, , help_text='When the address was geocoded. (UTC)')