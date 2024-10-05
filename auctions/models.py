from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # ********PRIMARY KEY********: AbstractUser: user_id
    # watchlist
    # ********FOREIGN KEYS********:
    # none
    watchlist = models.ManyToManyRel("Auction_listing", related_name="watched_by", blank=True)


class Category(models.Model):
    title = models.CharField(max_length=25)
    
    # return number of items in category
    def item_count(self):
        return self.listings.count()

    # string represntation of category
    def __str__(self):
        return self.title

    # ********PRIMARY KEY********: category_id
    #   title
    #   item count


class Bid(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # listing = models.ForeignKey(Auction_Listing, on_delete=models.PROTECT, related_name="bids")
    # if User is deleted, delete the user's bid records
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # ********PRIMARY KEY********: bid_id
    # timestamp
    # amount
    # ********FOREIGN KEYS********:
    #   listing
    #   user


class Auction_Listing(models.Model):
    title = models.CharField(max_length = 25)
    description = models.TextField()
    # if Category or Category or Bid is deleted, do not proceed as long as a listing exists for them
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="listing")
    current_bid = models.ForeignObject(Bid, on_delete=models.PROTECT, related_name="listing")
    # if User is deleted, delete related auction_listings 
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    quantity = models.IntegerField
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
        
    #***PRIMAR KEY***: listing_id
    # title:                charfield
    # description:          textfield
    # quantity:             int
    # price:                float
    # timestamp listed:     timestamp now
    # closing date          date time field
    # bool open / closed    bool false    
    # ********FOREIGN KEYS********:
    #   user_id
    #   category_id


class Comment(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # if user or listing is deleted, delete comments
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    # ********PRIMARY KEY********: comment_id
    # timestamp
    # content
    # ********FOREIGN KEYS********:
    #   user_id
    #   listing_id
    #   bid_id