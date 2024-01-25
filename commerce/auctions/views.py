from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listings, Bids, Comments

class NewBidForm(forms.Form):
    bid = forms.DecimalField(
        label="", 
        max_digits=10, 
        decimal_places=2,  
        widget=forms.TextInput(attrs={'name':'bid', 'placeholder': 'Bid', 'class':"form-control"})
        )

def index(request):
    active_listings = Listings.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings":active_listings
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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


def create_listing(request):
    categories = ["Fashion", "Electronics", "Toys", "Home", "Beauty", "Sports", "Art", "Collectibles", "Baby"]
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        if 'category' in request.POST:
            category = request.POST["category"]
        else:
            category = None
        user = request.user.username
        new_listing = Listings(title=title, description=description, price=price, image_url=image, category=category, owner=user)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else: 
        categories.sort()
        if request.user.is_authenticated:
            return render(request, "auctions/create_listing.html",{
                "categories": categories
            })
        else:
            return HttpResponseRedirect(reverse("login"))


def listing_details(request, id):
    listing = Listings.objects.get(pk=id)
    bids = Bids.objects.filter(listing_id=id)
    last_bidder = bids.order_by('-created_at').first().bidder
    comments = Comments.objects.filter(listing_id=id).order_by('-created_at')
    if request.method == "POST":
        if "bid" in request.POST:
            bid_form = NewBidForm(request.POST)
            if bid_form.is_valid():
                bid = bid_form.cleaned_data["bid"]
                if len(bids) > 0 and bid <= listing.price:
                    message = "Your bid must be greater than the current bid"
                    return render(request, "auctions/listing_page.html", {
                        "details": listing,
                        "bids": len(bids),
                        "bid_form": bid_form,
                        "bid_message": message,
                        "last_bidder": last_bidder,
                        "comments": comments
                    })
                elif len(bids) == 0 and bid < listing.price:
                    message = "Your bid must be at least as large as the starting bid"
                    return render(request, "auctions/listing_page.html", {
                        "details": listing,
                        "bids": len(bids),
                        "bid_form": bid_form,
                        "bid_message": message,
                        "comments": comments
                    })
                else: 
                    # Add new bid to Bids Table
                    new_bid = Bids(bid_price=bid, bidder=request.user.username, listing_id=listing)
                    new_bid.save()
                    # Update listing's price 
                    listing.price = bid
                    listing.save()
                    return HttpResponseRedirect(reverse("details", args=[id]))
            else:
                bid_form.errors.clear()
                message = "Please enter a number"
                return render(request, "auctions/listing_page.html", {
                    "details": listing,
                    "bids": len(bids),
                    "bid_form": bid_form,
                    "bid_message":message,
                    "last_bidder": last_bidder,
                    "comments": comments
                })
        elif "comment" in request.POST:
                comment = request.POST["comment"]
                if not comment:
                    message = "Your comment cannot be blank."
                    return render(request, "auctions/listing_page.html", {
                    "details": listing,
                    "bids": len(bids),
                    "bid_form": NewBidForm(),
                    "last_bidder": last_bidder,
                    "comments": comments,
                    "comment_message": message
                })
                else:
                    new_comment = Comments(comment=comment, commenter=request.user.username, listing_id=listing)
                    new_comment.save()
                    return HttpResponseRedirect(reverse("details", args=[id]))
    else:
        if request.user.is_authenticated:
            return render(request, "auctions/listing_page.html", {
            "details": listing,
            "bids": len(bids),
            "bid_form": NewBidForm(),
            "last_bidder": last_bidder,
            "comments": comments
        })
        else:
            return HttpResponseRedirect(reverse("login"))
        
def close_bid(request, id):
    # Update listing to closed
    listing = Listings.objects.get(pk=id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect((reverse("details", args=[id])))

def watchlist(request):
    return render(request, "auctions/watchlist.html")