from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_Listing, Bid, Category, Comment
from . import util_functions


def index(request):
    # filter out and sort categories with listings
    categories = Category.objects.order_by('title')

    return render(request, "auctions/index.html", {
        "categories":categories,
        "listings":Auction_Listing.objects.all(),
    })


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


# todo selling and bids are very similar - combine?
def selling(request):
    if request.user.is_authenticated:
        selling = Auction_Listing.objects.filter(seller=request.user) 
        message = ""
            
        if not selling.exists():
            message = "No active listings found"
        return render(request, "auctions/selling.html", {
            "selling": selling,
            "message": message,
        })


def bids(request):
    if request.user.is_authenticated:
        bids = Bid.objects.filter(user=request.user)
        message = ""
        # listings = Bid.objects.filter(Auction_Listing.)

        if not bids.exists():
            message = "You have not bid on any listings yet."

        return render(request, "auctions/bids.html", {
            "bids": bids,
            "message": message
        })


def purchases(request):
    return render(request,"auctions/purchases.html")


def sell(request):
    return render(request, "auctions/sell.html")
        

def watchlist(request):
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all()
    else:
        watchlist = []
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "message": "No items in watchlist."
    })


def listing_detail(request, listing_id):
    listing = Auction_Listing.objects.get(id=listing_id)
    price = listing.price
    seller = listing.seller
    message = ""

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "toggle_watchlist":
            listing_id = request.POST["listing_id"]
            message = util_functions.toggle_watchlist(request.user, listing_id)
        
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
        "seller":seller,
        "message": message
    })


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = Auction_Listing.objects.filter(category=category)
    
    return render(request, "auctions/category_detail.html", {
        "category": category,
        "listings": listings,
    })


def categories(request):
    categories = Category.objects.all().order_by('title')
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })

