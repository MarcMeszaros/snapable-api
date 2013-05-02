from django.db import models

class ApiAccount(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'api'

    email = models.EmailField(help_text='The email contact for the API.')
    company = models.CharField(max_length=255, null=True, help_text='The name of the organization or company.')
    created = models.DateTimeField(auto_now_add=True, help_text='When the api account was created. (UTC)')

    def __unicode__(self):
        return str({
            'email': self.email,
            'company': self.company,
            'created': self.created,
            'pk': self.pk,
        })