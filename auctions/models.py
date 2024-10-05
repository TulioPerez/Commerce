from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # ********PRIMARY KEY********: AbstractUser: user_id
    # watchlist
    # ********FOREIGN KEYS********:
    # none
    pass


class Auction_Listing():
    #***PRIMAR KEY***: listing_id
    # title
    # description
    # quantity
    # price
    # timestamp listed
    # closing date
    # bool open / closed
    # ********FOREIGN KEYS********:
    #   user_id
    #   category_id
    #   bid_id
    pass


class Bid():
    # ********PRIMARY KEY********: bid_id
    # timestamp
    # amount
    # ********FOREIGN KEYS********:
    #   listing
    #   user
    pass


class Comment():
    # ********PRIMARY KEY********: comment_id
    # timestamp
    # content
    # ********FOREIGN KEYS********:
    #   user_id
    #   listing_id
    pass


class Category():
    # ********PRIMARY KEY********: category_id
    #   title
    #   item count
    pass