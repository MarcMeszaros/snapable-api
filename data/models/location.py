# django/tastypie/libs
from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# snapable
from data.models import Event

@python_2_unicode_compatible
class Location(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    event = models.ForeignKey(Event)

    address = models.CharField(max_length=255, help_text='The event address.')
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0, help_text='The address latitude.') # +/- 180.123456, accuracy: 0.111 m (ie. 11.1cm)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0, help_text='The address longitude.') # +/- 180.123456, accuracy: 0.111 m (ie. 11.1cm)

    def __str__(self):
        return '{0} - [{1}] {2}'.format(self.pk, self.event.url, self.address)

    def __repr__(self):
        return str({
            'address': self.address,
            'event': self.event,
            'lat': self.lat,
            'lng': self.lng,
        })

class LocationAdmin(admin.ModelAdmin):
    pass

#admin.site.register(Location, LocationAdmin)
