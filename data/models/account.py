from django.db import models

from data.models import Package
from data.models import User

class Account(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    admin = models.ForeignKey(User)
    package = models.ForeignKey(Package)
