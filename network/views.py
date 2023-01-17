from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
import json
import datetime
from django.core.paginator import Paginator
from .models import User, Post, Follow, Like


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    

def index(request):
    if request.user.is_authenticated:

        #Check if user has submitted the form
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = Post()
                post.text = form.cleaned_data["text"]
                date_time = datetime.datetime.now()
                post.date_time = date_time.strftime("%c")
                post.author = request.user
                post.save()
                return HttpResponseRedirect(reverse("index"))

        #Display all the posts to the user
        likes = Like.objects.all()
        liked_by_user = []

        try:
            for like in likes:
                if like.user.id == request.user.id:
                    liked_by_user.append(like.post.id)
        except:
            liked_by_user = []

        posts = Post.objects.all()
        p = Paginator(posts.order_by('-date_time'), 10)
        page = request.GET.get('page')
        posts_paginated = p.get_page(page)
        return render(request, "network/index.html", {
            "form": PostForm(),
            "posts_paginated": posts_paginated,
            "liked_by_user": liked_by_user
        })
    else:
        #Display a blank index if the user is not authenticated
        return render(request, "network/index.html")


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


def user_info(request, user_id):
    user = User.objects.get(id=user_id)
    user_posts = user.posts.all()
    followers = user.followers.all().count()
    following = user.following.all().count()
    if Follow.objects.filter(user_id=request.user, user_followed=user):
        isFollowing = True
    else:
        isFollowing = False
    
    return render(request, 'network/user.html', {
    "profile_user": user,
    "posts": user_posts.order_by('-date_time'),
    "isFollowing": isFollowing,
    "followers": followers,
    "following": following
    })


def handle_follow(request):
    name = request.POST["profile_user"]
    profile_user = User.objects.get(username = name)
    f = Follow()
    f.user = request.user
    f.user_followed = profile_user
    f.save()
    return HttpResponseRedirect(reverse(user_info, kwargs={'user_id': profile_user.id}))


def handle_unfollow(request):
    name = request.POST["profile_user"]
    profile_user = User.objects.get(username=name)
    Follow.objects.filter(user=request.user, user_followed=profile_user).delete()
    return HttpResponseRedirect(reverse(user_info, kwargs={'user_id': profile_user.id}))


def display_following(request):  
    user = request.user
    followed_users = Follow.objects.filter(user=user)
    posts = Post.objects.all()
    followed_posts = []

    for post in posts:
        for user in followed_users:
            if post.author == user.user_followed:
                followed_posts.append(post)


    p = Paginator(followed_posts, 10)
    page = request.GET.get('page')
    posts_paginated = p.get_page(page)
    return render(request, "network/following.html", {
        "followed_posts": followed_posts,
        "posts_paginated": posts_paginated
    })


def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        post_to_edit = Post.objects.get(pk=post_id)
        post_to_edit.text = data["text"]
        post_to_edit.save()
        return JsonResponse({"message": "Change successful", "data": data["text"]})


def add_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    newLike = Like(user=user, post=post)
    newLike.save()
    return JsonResponse({"message": "Like added!"})


def delete_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    Like.objects.filter(user=user, post=post).delete()
    return JsonResponse({"message": "Like deleted!"})