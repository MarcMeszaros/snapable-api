from django.db import models

class User(models.Model):

    class Meta:
        app_label = 'data'

    # the model fields
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    billing_zip = models.CharField(max_length=11)
    terms = models.BooleanField(default=False)
    #user_type = models.PositiveSmallIntegerField(max_length=2, choices=USER_TYPE_CHOICES, default=TYPE_CREATOR)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_access = models.DateTimeField(auto_now_add=True)
