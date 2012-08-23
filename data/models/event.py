from django.db import models

from data.models import Package
from data.models import Type
from data.models import User

class Event(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'
    
    user = models.ForeignKey(User)
    package = models.ForeignKey(Package)
    type = models.ForeignKey(Type)

    cover = models.IntegerField(default=0, help_text='Integer data. The photo ID of the image to use for the event cover.') # dirty hack... fix this...

    start = models.DateTimeField(help_text='Event start time. (UTC)')
    end = models.DateTimeField(help_text='Event end time. (UTC)')
    title = models.CharField(max_length=255, help_text='Event title.')
    url = models.CharField(max_length=255, help_text='A "short name" for the event.')
    pin = models.CharField(max_length=255, help_text='Pseudo-random PIN used for private events.')
    creation_date = models.DateTimeField(auto_now_add=True, help_text='When the event created. (UTC)')
    last_access = models.DateTimeField(auto_now_add=True, help_text='When the event was last accessed. (UTC)')
    access_count = models.IntegerField(default=0)
    enabled = models.BooleanField(help_text='Is the event considered "active" in the system.')