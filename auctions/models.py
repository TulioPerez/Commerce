from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction_Listing", related_name="watched_by", blank=True)


class Category(models.Model):
    title = models.CharField(max_length=25)
    
    # return number of items in category
    def item_count(self):
        return self.listings.count()

    # string represntation of category
    def __str__(self):
        return self.title


class Auction_Listing(models.Model):
    # todo add listing date timestamp
    title = models.CharField(max_length = 25)
    description = models.TextField()
    # if Category or Category or Bid is deleted, do not proceed as long as a listing exists for them
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="listings")
    current_bid = models.ForeignKey("Bid", on_delete=models.PROTECT, related_name="listings", null=True, blank=True)
    # if User is deleted, delete related auction_listings 
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField(blank=False)
    is_open = models.BooleanField(default=True)

    # allow user to close an auction
    def close_auction(self):
        self.is_open = False
        self.save()

    # returns True when auction has expired
    def has_ended(self):
        return not self.is_open or timezone.now() >= self.closing_date

    def __str__(self):
        return f"{self.id}: Title: {self.title}"


class Bid(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # if User is deleted, delete the user's bid records
    listing = models.ForeignKey(Auction_Listing, on_delete=models.PROTECT, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # if user or listing is deleted, delete comments
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
