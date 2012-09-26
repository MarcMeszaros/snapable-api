from django.db import models

class Addon(models.Model):
    
    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'

    title = models.CharField(max_length=255, help_text='The title of the addon.')
    description = models.TextField(help_text='The addon description.')
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text='The per unit adddon price.') # 9999.99
    enabled = models.BooleanField(default=True, help_text='If the addon is enabled or not.')