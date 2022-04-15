from django.db import models
from django.utils.translation import gettext_lazy as _

class Bid(models.Model):

    bidder = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    auction = models.ForeignKey('auctions.Auction', on_delete=models.CASCADE)
