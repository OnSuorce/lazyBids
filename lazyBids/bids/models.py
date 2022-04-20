from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

class Bid(models.Model):

    bidder = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    auction = models.ForeignKey('auctions.Auction', on_delete=models.CASCADE)

    publish_date =  models.DateField(auto_now_add=True, editable=False)

    has_won = models.BooleanField(default=False)

    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)

    def __str__(self):
        return f"{self.bidder} - {self.amount} - {self.auction}"