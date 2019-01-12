from ..models import Retweet,Tweet
from django import template
from django.contrib.auth.models import User
register = template.Library()

@register.filter
def has_retweeted(tweet_id,user_id):
    tweet = Tweet.objects.get(id = tweet_id)
    user = User.objects.get(id = user_id)
    print(user)
    user_ids = tweet.retweets.all().values_list("user_id",flat  = True)
    print(user_ids)
    if user.id in user_ids:
        print(True)
        return True

    else: 
        return False