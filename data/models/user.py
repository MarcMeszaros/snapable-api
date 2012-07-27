import bcrypt
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import (check_password, make_password, is_password_usable)

class User(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    # the model fields
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    billing_zip = models.CharField(max_length=11)
    terms = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_access = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password, hasher='pbkdf2_sha256'):
        #if hasher == 'bcrypt':
        #    self.password = make_password(raw_password, hasher='bcrypt')
        if hasher == 'pbkdf2_sha256':
            self.password = make_password(raw_password, hasher='pbkdf2_sha256')
        else:
            self.password = make_password(raw_password, hasher='pbkdf2_sha256')
