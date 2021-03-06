from django.shortcuts import render,redirect,get_object_or_404
from .models import Tweet,Tag,Retweet,Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from authentication.models import Profile
from django.db.models import Count
from .forms import TweetForm,CommentForm
from django.contrib.postgres.search import SearchRank, SearchVector, SearchQuery
from django.contrib import messages
import re
from django.contrib.auth.models import User
from actions.models import Action
from  actions.utils import add_action
import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
# Create your views here.

@login_required
def home(request,id = None):
    # to get the ids for the users the curent user is following
    ids = request.user.profile.following.all().values_list("id",flat=True)
    user_ids = [id for id in ids]
    # add the id of the current user to include the tweets by the current user
    user_ids.append(request.user.id)
    # get all the tweets and retweets and add them to one array
    tweets = Tweet.objects.filter(user_id__in = user_ids)
    retweets = Retweet.objects.filter(user__in = user_ids)
    all_tweets = []
    for tweet in tweets:
        all_tweets.append(tweet)
    for tweet in retweets:
        all_tweets.append(tweet)
    # sort all by pub_date
    all_tweets.sort(key=lambda u:u.pub_date,reverse = True)
    # get related items to avoid multiple db queries
    tweets.select_related("user","comments").prefetch_related("likes","retweets","tags  ")

    # users
    users = Profile.objects.all().exclude(user_id__in = user_ids).order_by("-followers_count")

    form = CommentForm()

    context = {
        "tweets":all_tweets,
        "users": users,
        "form":form,
        "section":"home"
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
    add_action(user = request.user,action = "liked a " ,target = tweet)
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
                num_tweets = db_tag.num_of_tweets
                num_tweets += 1
                db_tag.num_of_tweets = num_tweets
                db_tag.save()

            latest_tweet.save()
            print(latest_tweet.tags.all())


 
            return redirect("home")
    else:
        form = TweetForm()

    return render(request,"tweets/add.html",{"form":form})

def retweet(request):
    tweet_id = request.POST.get("id")

    retweet,created = Retweet.objects.get_or_create(tweet_id = tweet_id, user = request.user)

    if not created:
        retweet.delete()
        retweeted = False
    else:
        retweeted = True

    data = {
        "retweeted":retweeted,
        "count": retweet.tweet.retweets.all().count(),
        "user_retweets":request.user.retweets.all().count()
    }
    add_action(user = request.user, action = "retweeted a tweet by " ,target = retweet.tweet.user)
    return JsonResponse(data)

def add_comment(request):
    user_id = int(request.POST.get("user_id"))
    tweet_id = int(request.POST.get("tweet_id"))
    tweet = Tweet.objects.get(id = tweet_id)
    user = User.objects.get(id = user_id)

    Comment.objects.create(content = request.POST.get("content"),user = user, tweet = tweet)

    data = {
        "count":tweet.comments.all().count(),
        'status':'ok'
    }

    add_action(user = user ,target = tweet,action = "commented on" )
    return JsonResponse(data)

def single_tweet(request,tweet_id):
    tweet = get_object_or_404(Tweet,id = tweet_id)

    context = {
        "tweet":tweet
    }

    return render(request,"tweets/single.html",context)

def search(request):
    context = {}
    if "query" in request.GET:
        query = request.GET.get("query")
        # search for tweets,users and tags

        #######TAGS#########
        #this will get all the tags which contain the search term and order by the ones with the most tweets associated with them
        tags = Tag.objects.filter(name__icontains = query).order_by("-num_of_tweets")


        ######users########
        # we'll want to search for users based on their email,username of any of their names
        search_query = SearchQuery(query)
        search_vectors = SearchVector("email",weight = "C") + SearchVector("email",weight = "B") + SearchVector("first_name",weight = "A") + SearchVector("last_name",weight = "A") + SearchVector("username",weight = "A")

        users = User.objects.annotate(rank = SearchRank(search_vectors,search_query)).filter(rank__gte = 0.1)


        ###### Tweets #####
        # search by the content,users who posted
        search_query = SearchQuery(query)
        search_vectors = SearchVector("username",weight = "A") + SearchVector("content",weight = "A")

        tweets = Tweet.objects.annotate(rank = SearchRank(search_vectors,search_query)).filter(rank__gte = 0.1)
    
        context = {
            "tweets":tweets,
            "tags":tags,
            "users":users
        }
    return render(request,"tweets/search.html",context)


