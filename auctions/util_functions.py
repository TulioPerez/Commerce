from django.shortcuts import render
from .models import User, Auction_Listing, Bid, Category, Comment


def is_user_listing(request, user, listing_id):
    # if listing created by (logged_in) user 
    pass


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

    # details about a single listing showing current bid
    # if user logged in, they can add it to their "watchlist"
    # if item is already in watchlist, user can remove it
    # if logged in, user can bid on item that is not theirs
    #     bid must be at least as much as starting bid 
    #     additional bids should be greater than current bid
    #         else error message

    # if logged in & user created the listing: 
    #     ability to "close" the auction
    #     current (highest) bid, if any, is the winner of the auction
    #         listing is no longer available (archive?)