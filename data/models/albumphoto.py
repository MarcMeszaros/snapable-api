# django/libs
from django.db import models

class AlbumPhoto(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    album = models.ForeignKey('Album')
    photo = models.ForeignKey('Photo')