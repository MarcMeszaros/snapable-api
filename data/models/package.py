from django.db import models

class Package(models.Model):

    # required to make 'south' migrations work
    class Meta:
        app_label = 'data'
    
    short_name = models.CharField(max_length=255, help_text='The package short name.')
    name = models.CharField(max_length=255, help_text='The package long name.')
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text='The package price.') # 9999.99
    prints = models.IntegerField(help_text='The number of free prints included in the package.')
    additional_price_per_print = models.DecimalField(max_digits=6, decimal_places=2, help_text='The price for each additional print.') # 9999.99
    albums = models.IntegerField(help_text='The number of albums included in the package.')
    slideshow = models.BooleanField(help_text='If the slideshow feature enabled.')
    shipping = models.BooleanField(help_text='If shipping included.')
    table_cards = models.BooleanField(help_text='If table cards are included.')
    guest_reminders = models.BooleanField(help_text='If guest reminders are included.')
    enabled = models.BooleanField(help_text='If the package is enabled.')