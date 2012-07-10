from django.db import models

class Package(models.Model):
    
    class Meta:
        app_label = 'data'

    short_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2) # 9999.99
    prints = models.IntegerField()
    additional_price_per_print = models.DecimalField(max_digits=6, decimal_places=2) # 9999.99
    albums = models.IntegerField()
    slideshow = models.BooleanField()
    shipping = models.BooleanField()
    table_cards = models.BooleanField()
    guest_reminders = models.BooleanField()
    enabled = models.BooleanField()