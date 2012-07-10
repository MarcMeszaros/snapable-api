from django.db import models
from api.data.models.album import Album
from api.data.models.photo import Photo

class AlbumPhoto(models.Model):
    
    class Meta:
        app_label = 'data'

    album = models.ForeignKey(Album)
    photo = models.ForeignKey(Photo)