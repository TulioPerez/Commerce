from .models import User, Auction_Listing, Bid, Category, Comment


def is_user_listing(request, user, listing_id):
    # if listing created by (logged_in) user 
    pass


def bid(bid):
    if listing_is_open and not user_is_seller() and bid > Auction_Listing.price:
        Auction_Listing.price = bid
        Auction_Listing.price.save()


def listing_is_open():
    return Auction_Listing.is_open


def user_is_seller():
    return User.id == Auction_Listing.seller.id


def toggle_watchlist(user, listing_id):
    watchlist = user.watchlist.all()
    listing = Auction_Listing.objects.get(id=listing_id)

    if listing in watchlist:
        user.watchlist.remove(listing)
        return {"message": "Item added from watchlist."}
    else:
        user.watchlist.add(listing)
        user.save()
        return {"message": "Item added from watchlist."}
    
        


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