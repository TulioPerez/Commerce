from datetime import timedelta
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction


class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction_Listing", related_name="watched_by", blank=True)
    purchases = models.ManyToManyField("Auction_Listing", related_name="purchased_by", blank=True)


class Category(models.Model):
    title = models.CharField(max_length=25)
    
    # return number of items in category
    def item_count(self):
        return self.listings.count()

    # string represntation of category
    def __str__(self):
        return self.title


class Auction_Listing(models.Model):
    # if Category or Category or Bid is deleted, do not proceed as long as a listing exists for them
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="listings")
    title = models.CharField(max_length = 25)
    description = models.TextField()
    image = models.FileField(upload_to="media/", blank=False, default="media/placeholder.jpg")
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.ForeignKey("Bid", on_delete=models.PROTECT, related_name="listings", null=True, blank=True)
    # if User is deleted, delete related auction_listings 
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    timestamp = models.DateTimeField(auto_now_add=True)
    closing_time = models.DateTimeField(blank=False)
    is_open = models.BooleanField(default=True)

    # close auction
    def close_auction(self):
        if self.is_open:
            with transaction.atomic():
                self.is_open = False
                self.save()    

                print(f"****Current BID = {self.current_bid} USER = {self.current_bid.user}\n")    

                if self.current_bid:
                    user = self.current_bid.user
                    print(f"HIGHEST BIDDER = {user}")
                    user.purchases.add(self)
                    user.save()

    # returns True when auction has expired
    def has_ended(self):
        return not self.is_open or timezone.now() - timedelta(hours = 4) >= self.closing_time

    def __str__(self):
        return f"{self.id}: Title: {self.title}"


class Bid(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # if User is deleted, delete the user's bid records
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.PROTECT, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Comment(models.Model):
    # if user or listing is deleted, delete comments
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
