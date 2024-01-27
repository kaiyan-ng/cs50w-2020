from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.TextField()
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image_url = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    owner = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "active" if self.active else "closed"
        return f"Listing {self.id}: {self.title} is {status} with a starting price of {self.price}"

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
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'listing')
        """ensures that each combination of user and listing is unique in the database. 
        This means that a user cannot add the same listing to their watchlist multiple times. """
