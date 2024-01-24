from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.TextField()
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image_url = models.TextField(null=True)
    category = models.TextField(null=True)
    owner = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "active" if self.active else "closed"
        return f"Listing {self.id}: {self.title} is {status} with a starting price of {self.starting_price}"

class Bids(models.Model):
    bid_price = models.DecimalField(max_digits=10,decimal_places=2)
    bidder = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)

    def __str__(self):
        return f"Listing {self.listing_id}: {self.bidder} made a bid of {self.bid_price}"

class Comments(models.Model):
    comment = models.TextField()
    commenter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    listing_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Listing {self.listing_id}: {self.commenter} added a comment - {self.comment}"
