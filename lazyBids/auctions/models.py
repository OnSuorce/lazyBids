
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Create your models here.
class Auction(models.Model):

    title = models.TextField(null=False, max_length=100)

    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    
    description = models.TextField(max_length=500, null=False)
    
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2)

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, blank=False, null=False)
    
    image_url = models.URLField(null=False)
    
    publish_date = models.DateField(auto_now_add=True, editable=False)

    is_open = models.BooleanField(default=True)

    currency = models.CharField(max_length=3, choices=settings.CURRENCIES, default="USD")

    last_updated = models.DateField(auto_now=True, editable=False)

    def __str__(self):
        
        return f"{self.pk} - {self.title}"