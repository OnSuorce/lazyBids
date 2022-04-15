from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Auction(models.Model):

    title = models.TextField(null=False, max_length=100)
    description = models.TextField(max_length=500, null=False)
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2)

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, blank=False, null=False)
    
    image_ulr = models.URLField(null=False)
    
    publish_date = models.DateField(auto_now_add=True, editable=False)

    is_open = models.BooleanField(default=True)

    CURRENCIES = (
            ('USD', 'U.S. Dollar'),
            ('EUR', 'European Euro'),
            ('JPY', 'Japanese Yen'),
            ('GBP', 'British Pound'),
            ('CHF', 'Swiss Franc'),
            ('JPY', 'Japanese Yen'),
            ('CAD', 'Canadian Dollar'),
            ('AUD', 'Australian Dollar'),
            ('ZAR', 'South African Dollar'),
            ('CNY', 'Renminbi'),
            ('RUB', 'Russian Ruble'),
        )
    currency = models.CharField(max_length=3, choices=CURRENCIES)