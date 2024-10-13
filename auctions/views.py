from django.utils import timezone
from datetime import datetime, timedelta
from django import forms
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import ListingForm
from .models import Auction_Listing
from django.db import transaction


from .models import User, Auction_Listing, Bid, Category
# , Comment
from . import util_functions


# todo :
# Add commenting

# When listing expired:
#   remove from active listings in index (no longer use: objects.all() in index)
#   grey out listing in "my listings" and precede by "closed"
#   no Bid / watchlist button

# details about a single listing showing current bid
# if logged in, user can bid on item that is not theirs
#     bid must be at least as much as starting bid 
#     additional bids should be greater than current bid
#         else error message

# if logged in & user created the listing: 
#     ability to "close" the auction
#     current (highest) bid, if any, is the winner of the auction
#         listing is no longer available (archive?)


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # todo make the page displayed once logged in == the item page
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def index(request):
    categories = Category.objects.order_by('title')

    return render(request, "auctions/index.html", {
        "categories":categories,
        "listings":Auction_Listing.objects.all(),
    })


def sell(request, listing_id=None):
    if request.method == "POST":
        # listing_id was provided - this is an edit to a listing
        if listing_id:
            listing = get_object_or_404(Auction_Listing, id=listing_id)
            form = ListingForm(request.POST, request.FILES, instance=listing)
        else:
        # no listing_id - create a new listing
            form = ListingForm(request.POST, request.FILES)

        if form.is_valid():
            # satisfy Auction_Listing's seller requirement  
            listing = form.save(commit=False)
            listing.seller = request.user

            # make closing time timezone-aware
            closing_time = form.cleaned_data['closing_time']
            if timezone.is_naive(closing_time):
                closing_time = timezone.make_aware(closing_time)

            #  ensure that closing time is in the future and account for server difference
            if closing_time <= timezone.now() - timedelta(hours = 4):
                return render(request, "auctions/sell.html", {
                    'form': form,
                    'message': "Closing time must be set to a future time."
                })
            
            listing.closing_time = closing_time
            
            # close the auction if is_open was set to False
            if not listing.is_open:
                listing.close_auction()
                print("LISTING IS NOW CLOSED\n\nLISTING IS NOW CLOSED\n\nLISTING IS NOW CLOSED\n\nLISTING IS NOW CLOSED\n\n")
                listing.closing_time = timezone.now() - timedelta(hours = 4)

            form.save()
            return redirect('listing_detail', listing.id)

    else:
        # pre-populate form if editing
        if listing_id:
            listing = get_object_or_404(Auction_Listing, id=listing_id)
            form = ListingForm(instance=listing)
        else:
            form = ListingForm()

    return render(request, "auctions/sell.html", {'form': form})


# todo selling and bids are very similar - combine?
def selling(request):
    if request.user.is_authenticated:
        listings = Auction_Listing.objects.filter(seller=request.user) 
        message = ""
            
        if not listings.exists():
            message = "No active listings found"
        return render(request, "auctions/selling.html", {
            "listings": listings,
            "message": message,
        })


def bids(request):
    if request.user.is_authenticated:
        bids = Bid.objects.filter(user=request.user).order_by('listing__closing_time')
        # .order_by('listing__title')
        message = ""
        # listings = Bid.objects.filter(Auction_Listing.)

        if not bids.exists():
            message = "You have not bid on any listings yet."

        return render(request, "auctions/bids.html", {
            "bids": bids,
            "message": message
        })


def purchases(request):
    if request.user.is_authenticated:
        purchases = request.user.purchases.all()
    else:
        purchases = []

    return render(request,"auctions/purchases.html", {
        "purchases": purchases
    })


def watchlist(request):
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all().order_by('title')
    else:
        watchlist = []
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "message": "No items in watchlist."
    })


def listing_detail(request, listing_id):
    # todo use GETin this format for all functions:
    listing = get_object_or_404(Auction_Listing, id=listing_id)
    price = listing.price
    seller = listing.seller
    message = ""
    bids = listing.bids.count()

    # unpack return values for countdown message and is_open state
    time_remaining_message, _ = util_functions.get_time_remaining(listing.closing_time)

    # close the auction if time has run out
    if (listing.has_ended() and listing.is_open):
        print("\n\n\n************** CLOSING THE AUCTION ************** \n\n\n\n")
        print(f"listing.hasended = {listing.has_ended}")

        listing.close_auction()
        print("\n\n\n************** AUCTION is now CLOSED ************** \n\n\n\n")


    # assign purchase to highest bidder, if any
    # if not listing.is_open and listing.current_bid:
    #     buyer = util_functions.get_buyer(listing.current_bid)
    #     buyer.purchases.add(listing)
    #     buyer.save()
    #     print(f"purchase added to {buyer}")

    if request.method == "POST":
        action = request.POST.get("action")
        # toggle watchlist
        if action == "toggle_watchlist":
            listing_id = request.POST["listing_id"]
            message = util_functions.toggle_watchlist(request.user, listing_id)
        # user bid 
        if action == "bid":
            bid_amount = Decimal(request.POST.get("bid_amount"))
            if bid_amount > listing.price:
                util_functions.bid(request.user, listing_id, bid_amount)
                listing.price = bid_amount
                message = "Congratulations, you've successfully submitted your bid!"
            else:
                message = f"Your bid amount must be higher than the current bid of {listing.price}"

    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "price": price,
        "bids": bids,
        "seller":seller,
        "message": message,
        "time_remaining_message": time_remaining_message,
    })


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = Auction_Listing.objects.filter(category=category, is_open=True)
    
    return render(request, "auctions/category_detail.html", {
        "category": category,
        "listings": listings,
    })


def categories(request):
    categories = Category.objects.all().order_by('title')
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })


class ImageUpload(forms.Form):
    title = forms.CharField()
    file = forms.FileField()

