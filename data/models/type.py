from django.db import models

class Type(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    # list of variables to int mappings
    TYPE_CREATOR = 1
    TYPE_BRIDE_GROOM = 2
    TYPE_WEDDING_PARTY = 3
    TYPE_FAMILY = 4
    TYPE_GUESTS = 5
    TYPE_PUBLIC = 6

    # create a list of choice tuple mappings, to human names
    TYPE_CHOICES = (
        (TYPE_CREATOR, 'Event Creator'),
        (TYPE_BRIDE_GROOM, 'Bride/Groom'),
        (TYPE_WEDDING_PARTY, 'Wedding party'),
        (TYPE_FAMILY, 'Family'),
        (TYPE_GUESTS, 'Guests'),
        (TYPE_PUBLIC, 'Public'),
    )

    name = models.CharField(max_length=255, help_text='The name of the TYPE value mapping.')

    def __unicode__(self):
        return str({
            'name': self.name,
        })