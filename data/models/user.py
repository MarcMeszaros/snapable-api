import bcrypt
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import (check_password, make_password, is_password_usable)

class User(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    # the model fields
    email = models.CharField(max_length=255, unique=True, db_index=True, help_text="The user's email.")
    password = models.CharField(max_length=255, help_text="The user's password parts.")
    first_name = models.CharField(max_length=255, help_text="The user's first name.")
    last_name = models.CharField(max_length=255, help_text="The user's last name.")
    billing_zip = models.CharField(max_length=11, help_text="The user's billing ZIP/Postal code.")
    terms = models.BooleanField(default=False, help_text='If the user accespted the Terms Of Service.')
    creation_date = models.DateTimeField(auto_now_add=True, help_text='When the user was created. (UTC)')
    last_access = models.DateTimeField(auto_now_add=True, help_text='When the user last accessed the system. (UTC)')
    payment_gateway_user_id = models.CharField(max_length=255, null=True, default=None, help_text='The user ID on the payment gateway linked to this user.')

    ## virtual properties getters/setters ##
    # return the number of photos related to this event
    def _get_name(self):
        return self.first_name + ' ' + self.last_name

    def _set_name(self, value):
        pass

    # add the virtual properties
    name = property(_get_name, _set_name)

    def __unicode__(self):
        return str({
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'billing_zip': self.billing_zip,
            'terms': self.terms,
        })

    def set_password(self, raw_password, hasher='pbkdf2_sha256'):
        self.password = generate_password(raw_password, hasher)

    @staticmethod
    def generate_password(raw_password, hasher='pbkdf2_sha256'):
        #if hasher == 'bcrypt':
        #    return make_password(raw_password, hasher='bcrypt')
        if hasher == 'pbkdf2_sha256':
            return make_password(raw_password, hasher='pbkdf2_sha256')
        else:
            return make_password(raw_password, hasher='pbkdf2_sha256')
