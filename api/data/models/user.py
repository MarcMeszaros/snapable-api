from django.db import models

class User(models.Model):

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
    USER_TYPE_CHOICES = (
        (TYPE_CREATOR, 'Event Creator'),
        (TYPE_BRIDE_GROOM, 'Bride/Groom'),
        (TYPE_WEDDING_PARTY, 'Wedding party'),
        (TYPE_FAMILY, 'Family'),
        (TYPE_GUESTS, 'Guests'),
        (TYPE_PUBLIC, 'Public'),
    )

    # the model fields
    email = models.CharField(max_length=255, unique=True)
    salt = models.CharField(max_length=40)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    billing_zip = models.CharField(max_length=11)
    terms = models.BooleanField(default=False)
    user_type = models.PositiveSmallIntegerField(max_length=2, choices=USER_TYPE_CHOICES, default=TYPE_CREATOR)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now_add=True)
