from django.utils import timezone
from datetime import timedelta, datetime
from django import views

from django.shortcuts import render
from .models import User, Auction_Listing, Bid, Category, Comment


def bid(user, listing_id, bid_amount):
    listing = Auction_Listing.objects.get(id=listing_id)
    if listing_is_open(listing) and not user_is_seller(user, listing):

        # save the bid to Bid table
        new_bid = Bid(user=user, listing=listing, amount=bid_amount)
        new_bid.save()

        listing.price = bid_amount
        listing.current_bid = new_bid
        listing.save()


# helper functions for bid
def listing_is_open(listing):
    return listing.is_open


# helper functions for bid
def user_is_seller(user, listing):
    return user == listing.seller



# for image uploads
def handle_image_upload(f, filename):
    with open(filename, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def toggle_watchlist(user, listing_id):
    watchlist = user.watchlist.all()
    listing = Auction_Listing.objects.get(id=listing_id)

    if listing in watchlist:
        user.watchlist.remove(listing)
        user.save()
        return "Item removed from watchlist."
    else:
        user.watchlist.add(listing)
        user.save()
        return "Item added to watchlist"


def get_time_remaining(closing_time):
    now = timezone.make_aware(datetime.now())
    # now = timezone.localtime(timezone.now())
    time_remaining = closing_time - now
    # print(f"time_remaining = {time_remaining}")

    #  if there is time remaining, get expiration message
    if time_remaining.total_seconds() > 0:
        days = time_remaining.days
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60
        seconds = time_remaining.seconds % 60
        return get_expiration_msg((days, hours, minutes, seconds))
    else:
        return  "Auction Closed", True


def get_expiration_msg(time_remaining):
    days, hours, minutes, seconds = time_remaining

    # days remaining
    if days >= 1: 
        return f"Closes in {days} days, {hours} hours, {minutes} minutes", False
    # hours remaining
    elif days == 0 and hours >= 1: 
        return f"Closes in {hours} hours, {minutes} minutes", False
    # 30+ minutes remaining
    elif minutes >=30: 
        return f"Closing in {minutes} minutes, {seconds} seconds.", False
    # final minutes remaining
    else: 
        return f"Hurry! Auction closing in {minutes} minutes, {seconds} seconds!", False


def get_buyer(bid):
    return bid.user