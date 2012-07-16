from django.db import models

from data.models import Album
from data.models import Photo

class AlbumPhoto(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    album = models.ForeignKey(Album)
    photo = models.ForeignKey(Photo)