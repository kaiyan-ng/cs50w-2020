import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Post, Follow
from django.core.paginator import Paginator

class NewPostForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":3, "style": "width: 100%;"}))

def index(request):
    posts = Post.objects.all().order_by('-created_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            new_post = Post(user=request.user, content=new_content)
            new_post.save()
            posts = Post.objects.all().order_by('-created_date')
            paginator = Paginator(posts, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "network/index.html", {
                "form": NewPostForm(),
                "pages": page_obj
            })
        else: 
           return render(request, "network/index.html", {
                "form": form,
                "pages": page_obj
            })
    else:
        return render(request, "network/index.html", {
            "form": NewPostForm(),
            "pages": page_obj
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def view_profile(request, id):
    profile_user = User.objects.get(pk=id)
    is_following = False
    if request.user.is_authenticated:
        acc_user = request.user
        # Check if profile does not belong to user 
        if not request.user.id == id:
            # Is user following the profile
            is_following = Follow.objects.filter(follower=acc_user, following=profile_user).exists()
    else:
        acc_user=None
    username = User.objects.get(pk=id).username
    posts = Post.objects.filter(user=User.objects.get(pk=id)).order_by('-created_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    followers = Follow.objects.filter(following=profile_user).count()
    followings = Follow.objects.filter(follower=profile_user).count()
    return render(request, "network/profile.html", {
        "user_id": id,
        "username": username,
        "pages": page_obj,
        "follow": is_following,
        "followers": followers,
        "followings": followings
    })

@login_required
def follow(request, id):
    new_follower = User.objects.get(pk=request.user.id)
    new_following = User.objects.get(pk=id)
    new_following = Follow(follower=new_follower, following=new_following)
    new_following.save()
    return HttpResponseRedirect(reverse("profile", kwargs={'id': id}))

@login_required
def unfollow(request, id):
    follower = User.objects.get(pk=request.user.id)
    following = User.objects.get(pk=id)

     # Attempt to retrieve the Follow object
    follow_obj = Follow.objects.filter(follower=follower, following=following).first()

    # If the Follow object exists, delete it
    if follow_obj:
        follow_obj.delete()

    return HttpResponseRedirect(reverse("profile", kwargs={'id': id}))

@login_required
def view_following(request):
    followings = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    posts = Post.objects.filter(user__in=followings).order_by('-created_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "pages": page_obj
    })

@login_required
def post(request, post_id):
    # Query for requested post
    try:
       post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post details
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post content
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)
