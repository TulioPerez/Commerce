from datetime import timedelta
from django import views
from django.utils import timezone

from django.shortcuts import render
from .models import User, Auction_Listing, Bid, Category, Comment


def bid(user, listing_id, bid_amount):
    listing = Auction_Listing.objects.get(id=listing_id)
    if listing_is_open(listing) and not user_is_seller(user, listing):
        listing.price = bid_amount
        listing.save()

        # save the bid to Bid table
        new_bid = Bid(user=user, listing=listing, amount=bid_amount)
        new_bid.save()


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

def convert_time_remaining(closing_time):
    now = timezone.now()
    time_remaining = closing_time - now

    if time_remaining >= timedelta(days = 1):
        return f"Closes in {time_remaining.days} days, {time_remaining.seconds // 3600} hours"
    
    elif time_remaining >= timedelta(hours = 1):
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60
        return f"Closing in {hours} hours, {minutes} minutes"
    
    elif time_remaining >= timedelta(minutes = 1):
        minutes = time_remaining.seconds // 60
        seconds = time_remaining.seconds % 60
        return f"Hurry! Auction closes in {minutes} minutes, {seconds} seconds."
    
    else:
        return "Auction Closed"