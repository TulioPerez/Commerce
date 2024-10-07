from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction_Listing, Bid, Category, Comment


categories = Category.objects.order_by('title')

def index(request):
    # filter out and sort categories with listings

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


# todo add @login_required to prevent those NOT logged in from accessing (as per instruction hint)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def item_detail(request, listing_id):
    # is_mine if the user created this listing
    return render(request, "auctions/item_detail.html", {
        "listing_id": Auction_Listing.id
    })


# def listings(request):
#     return render(request, "listings.html")
    

# def category(request):
#     return render(request, "auctions/category.html")

# def category(request):
#     return render(request, "auctions/category.html")


def category(request):
    pass
    categories = Category.objects.all().order_by('title')
    return render(request, "auctions/category.html", {
        "categories": categories,
    })



def my_bids(request):
    pass