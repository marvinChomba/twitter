from django.shortcuts import render,redirect,get_object_or_404
from .models import Tweet,Tag,Retweet
from django.http import JsonResponse
from .forms import TweetForm
import re
# Create your views here.

def home(request):
    ids = request.user.profile.following.all().values_list("id",flat=True)
    user_ids = [id for id in ids]
    user_ids.append(request.user.id)
    tweets = Tweet.objects.filter(user_id__in = user_ids)
    retweets = Retweet.objects.filter(user__in = user_ids)
    all_tweets = []
    for tweet in tweets:
        all_tweets.append(tweet)
    for tweet in retweets:
        all_tweets.append(tweet)

    all_tweets.sort(key=lambda u:u.pub_date,reverse = True)
    tweets.select_related("user","comments").prefetch_related("likes","retweets","tags  ")

    context = {
        "tweets":all_tweets
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
        "count":tweet.likes.all().count(),
        "user_likes":request.user.likes.all().count()
    }
    return JsonResponse(data)

def add_tweet(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tags = re.findall("#\w+",form.cleaned_data["content"])
            print(tags)
            tags_without_hash = [re.sub("#","",tag) for tag in tags if len(tag) > 1]
            print(tags_without_hash)
            content = re.sub("#\w+","",form.cleaned_data["content"])
            tweet.content = re.sub("#","",content)
            tweet.save()
            latest_tweet = Tweet.objects.first()
            for tag in tags_without_hash:
                db_tag,created = Tag.objects.get_or_create(name=tag.lower())
                latest_tweet.tags.add(db_tag)

            latest_tweet.save()
            print(latest_tweet.tags.all())


 
            return redirect("home")
    else:
        form = TweetForm()

    return render(request,"tweets/add.html",{"form":form})

def retweet(requst):
    tweet_id = requst.POST.get("id")

    retweet,created = Retweet.objects.get_or_create(tweet_id = tweet_id, user = request.user)

    if not created:
        retweet.delete()
        retweeted = False
    else:
        retweeted = True

    data = {
        "retweeted":retweeted,
        "count": retweet.tweet.retweets.all().count()
    }
    return JsonResponse(data)