from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import fields
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Listing, User, Bid, Comment
from django import forms 

class create_form(forms.ModelForm):
    class Meta: 
        model = Listing
        fields = "__all__"

class bid_form(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["current_price"]

def index(request):
    return render(request, "auctions/index.html", {
        "data" : Listing.objects.all()
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

def product(request,name):
    return render(request, "auctions/product.html",{
        "data": Listing.objects.get(item_name = name)
    })
    
def watchlist(request):
    return render(request,"auctions/watchlist.html")

def categories(request):
    return render(request,"auctions/categories.html",{
        "list" : Listing.objects.values('item_category').distinct()
    })

def category(request,name):
    return render(request, "auctions/category.html",{
        "list" : Listing.objects.filter(item_category = name)
    })

def category_item(request,name,item_name):
    return(product(request,item_name))
    
def create(request):
    form = create_form(request.POST or None)
    if form.is_valid():
        form.save()
        return product(request,form.cleaned_data['item_name'])
    return render(request,"auctions/create.html",{
        "form" : create_form()
    })

def bid(request):
    form = bid_form(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request,"auctions/product.html",{
        "form" : bid_form()
    })