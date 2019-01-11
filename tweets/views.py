from django.shortcuts import render,redirect,get_object_or_404
from .models import Tweet
from django.http import JsonResponse
from .forms import TweetForm
# Create your views here.

def home(request):
    tweets = Tweet.objects.all()
    tweets.select_related("user","comments").prefetch_related("likes","retweets","tags  ")

    context = {
        "tweets":tweets
    }

    return render(request,"tweets/list.html",context)

def like(request):
    tweet_id = request.POST.get("id")
    tweet = Tweet.objects.get(id=int(tweet_id))
    
    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
        has_liked = True
    else:
        tweet.likes.add(request.user)
        has_liked = False

    data = {
        "has_liked":has_liked,
        "count":tweet.likes.all().count()
    }
    return JsonResponse(data)

def add_tweet(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("home")
    else:
        form = TweetForm()

    return render(request,"tweets/add.html",{"form":form})
