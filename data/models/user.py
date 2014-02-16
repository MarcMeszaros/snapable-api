# django/tastypie/libs
import bcrypt
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import (check_password, make_password, is_password_usable)
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.encoding import python_2_unicode_compatible

# snapable
import admin

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        user = self.model(email=UserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.model(email=UserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

@python_2_unicode_compatible
class User(AbstractBaseUser):

    # Django 1.5+ needs this defined
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    objects = UserManager()
    is_active = True

    # the model fields
    email = models.CharField(max_length=255, unique=True, db_index=True, help_text="The user's email.")
    #password = models.CharField(max_length=128, help_text="The user's password parts.")
    first_name = models.CharField(max_length=255, help_text="The user's first name.")
    last_name = models.CharField(max_length=255, help_text="The user's last name.")
    created_at = models.DateTimeField(auto_now_add=True, help_text='When the user was created. (UTC)')
    #last_login = models.DateTimeField(auto_now_add=True, help_text='When the user last accessed the system. (UTC)')
    payment_gateway_user_id = models.CharField(max_length=255, null=True, default=None, blank=True, help_text='The user ID on the payment gateway linked to this user.')

    ## virtual properties getters/setters ##
    # return the number of photos related to this event
    def _get_name(self):
        return self.first_name + ' ' + self.last_name

    def _set_name(self, value):
        pass

    # return the stripe credentials
    def _get_stripe_customer_id(self):
        return self.payment_gateway_user_id

    def _set_stripe_customer_id(self, value):
        self.payment_gateway_user_id = value

    # return if the current user is a staff
    def _get_is_staff(self):
        return self.pk < 1000

    def _set_is_staff(self, value):
        pass

    # return if the current user is a superuser
    def _get_is_superuser(self):
        return self.pk < 1000

    def _set_is_superuser(self, value):
        pass

    # add the virtual properties
    name = property(_get_name, _set_name)
    stripe_customer_id = property(_get_stripe_customer_id, _set_stripe_customer_id)
    created = property(_get_created, _set_created)
    is_staff = property(_get_is_staff, _set_is_staff)
    is_superuser = property(_get_is_superuser, _set_is_superuser)

    def __str__(self):
        return u'{0} ({1})'.format(self.name, self.email)

    def __repr__(self):
        return str({
            'created_at': self.created_at,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
        })

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.first_name

    @staticmethod
    def generate_password(raw_password, hasher='pbkdf2_sha256'):
        #if hasher == 'bcrypt':
        #    return make_password(raw_password, hasher='bcrypt')
        if hasher == 'pbkdf2_sha256':
            return make_password(raw_password, hasher='pbkdf2_sha256')
        else:
            return make_password(raw_password, hasher='pbkdf2_sha256')

    ### permissions ###
    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True
        else:
            return False

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True
        else:
            return False

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', 'created_at']
    readonly_fields = ['id', 'created_at', 'last_login']
    search_fields = ['email', 'first_name', 'last_name']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'email', 
                'password',
                ('first_name', 'last_name'),
                ('last_login', 'created_at'),
            ),
            'description': '<strong>NOTE: <em>A "plaintext" password in the "password" field will be hashed and saved and will overwrite the existing password.</em></strong>'
        }),
        ('Stripe', {
            'classes': ('collapse',),
            'fields': (
                'payment_gateway_user_id',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.password[:14] != 'pbkdf2_sha256$':
            obj.set_password(obj.password)
        obj.save()

admin.site.register(User, UserAdmin)
