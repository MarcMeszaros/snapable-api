from django.db import models
from api.data.models.user import User

class Event(models.Model):
    
    class Meta:
        app_label = 'data'

    user = models.ForeignKey(User)