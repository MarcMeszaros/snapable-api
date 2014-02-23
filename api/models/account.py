# django/tastypie/libs
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# snapable
import admin

@python_2_unicode_compatible
class ApiAccount(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'api'

    email = models.EmailField(help_text='The email contact for the API.')
    company = models.CharField(max_length=255, null=True, help_text='The name of the organization or company.')
    created = models.DateTimeField(auto_now_add=True, help_text='When the api account was created. (UTC)')

    def __str__(self):
        return '{0}'.format(self.company)

    def __repr__(self):
        return str({
            'email': self.email,
            'company': self.company,
            'created': self.created,
            'pk': self.pk,
        })

class ApiAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'company', 'created']
    readonly_fields = ['id', 'created']
    search_fields = ['email', 'company']
    fieldsets = (
        (None, {
            'fields': (
                'id',
                'email', 
                'company',
                'created',
            ),
        }),
    )

admin.site.register(ApiAccount, ApiAccountAdmin)
