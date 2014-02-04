# django/tastypie/libs
from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class ApiAccount(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'api'

    email = models.EmailField(help_text='The email contact for the API.')
    company = models.CharField(max_length=255, null=True, help_text='The name of the organization or company.')
    created = models.DateTimeField(auto_now_add=True, help_text='When the api account was created. (UTC)')

    def __str__(self):
        return '{0} - {1} ({2})'.format(self.pk, self.email, self.company)

    def __repr__(self):
        return str({
            'email': self.email,
            'company': self.company,
            'created': self.created,
            'pk': self.pk,
        })

class ApiAccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(ApiAccount, ApiAccountAdmin)
