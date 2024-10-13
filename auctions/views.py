from django.utils import timezone
from datetime import timedelta
from django import forms
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse
from .forms import ListingForm, CommentForm
from .models import Auction_Listing
from .models import User, Auction_Listing, Bid, Category
from . import util_functions


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
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
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# default page
def index(request):
    categories = get_list_or_404(Category.objects.order_by("title"))

    return render(
        request,
        "auctions/index.html",
        {
            "categories": categories,
            "listings": Auction_Listing.objects.all(),
        },
    )


# for listing creation
def sell(request, listing_id=None):
    if request.method == "POST":
        # listing_id was provided - this is an EDIT to a listing
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
            closing_time = form.cleaned_data["closing_time"]
            if timezone.is_naive(closing_time):
                closing_time = timezone.make_aware(closing_time)

            #  ensure that closing time is in the future and account for server difference
            if closing_time <= timezone.now() - timedelta(hours=4):
                return render(
                    request,
                    "auctions/sell.html",
                    {
                        "form": form,
                        "message": "Closing time must be set to a future time.",
                    },
                )
            listing.closing_time = closing_time

            # close the auction if is_open was set to False
            if not listing.is_open:
                listing.close_auction()
                listing.closing_time = timezone.now() - timedelta(hours=4)

            form.save()
            return redirect("listing_detail", listing.id)

    else:
        # re-populate form data when editing
        if listing_id:
            listing = get_object_or_404(Auction_Listing, id=listing_id)
            form = ListingForm(instance=listing)
        else:
            form = ListingForm()

    return render(request, "auctions/sell.html", {"form": form})


# for user - created listings
def selling(request):
    if request.user.is_authenticated:
        listings = Auction_Listing.objects.filter(seller=request.user)
        message = ""

        if not listings.exists():
            message = "No active listings found"
        return render(
            request,
            "auctions/selling.html",
            {
                "listings": listings,
                "message": message,
            },
        )


# for bids view
def bids(request):
    if request.user.is_authenticated:
        bids = Bid.objects.filter(user=request.user).order_by("listing__closing_time")
        message = ""

        if not bids.exists():
            message = "You have not bid on any listings yet."

        return render(request, "auctions/bids.html", {"bids": bids, "message": message})


# for user's successful purchases
def purchases(request):
    if request.user.is_authenticated:
        purchases = request.user.purchases.all()
    else:
        purchases = []

    return render(request, "auctions/purchases.html", {"purchases": purchases})


# for user's watchlist view
def watchlist(request):
    if request.user.is_authenticated:
        watchlist = request.user.watchlist.all().order_by("title")
    else:
        watchlist = []
    return render(
        request,
        "auctions/watchlist.html",
        {"watchlist": watchlist, "message": "No items in watchlist."},
    )


# detail view for listings
def listing_detail(request, listing_id):
    listing = get_object_or_404(Auction_Listing, id=listing_id)
    price = listing.price
    seller = listing.seller
    message = ""
    bids = listing.bids.count()
    comments = listing.comments.all()

    comment_form = CommentForm()

    # unpack return values for countdown message and is_open state
    time_remaining_message, _ = util_functions.get_time_remaining(listing.closing_time)

    # close the auction if time has run out
    if listing.has_ended() and listing.is_open:
        listing.close_auction()

    if request.method == "POST":
        action = request.POST.get("action")
        # watchlist functionality
        if action == "toggle_watchlist":
            listing_id = request.POST["listing_id"]
            message = util_functions.toggle_watchlist(request.user, listing_id)

        # bid functionality
        if action == "bid":
            bid_amount = Decimal(request.POST.get("bid_amount"))
            if bid_amount > listing.price:
                util_functions.bid(request.user, listing_id, bid_amount)
                listing.price = bid_amount
                message = "Congratulations, you've successfully submitted your bid!"
            else:
                message = f"Your bid amount must be higher than the current bid of {listing.price}"

        # comment functionality
        if action == "submit_comment":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.listing = listing
                comment.save()
                comment.message = "Comment added successfully"

    return render(
        request,
        "auctions/listing_detail.html",
        {
            "listing": listing,
            "price": price,
            "bids": bids,
            "seller": seller,
            "message": message,
            "time_remaining_message": time_remaining_message,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


# view that lists items within a category
def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = Auction_Listing.objects.filter(category=category, is_open=True)

    return render(
        request,
        "auctions/category_detail.html",
        {
            "category": category,
            "listings": listings,
        },
    )


# view that lists all categories
def categories(request):
    categories = Category.objects.all().order_by("title")
    return render(
        request,
        "auctions/categories.html",
        {
            "categories": categories,
        },
    )


# class for listing's image
class ImageUpload(forms.Form):
    title = forms.CharField()
    file = forms.FileField()
