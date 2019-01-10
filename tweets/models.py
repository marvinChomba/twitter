from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User,related_name='tweets',on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User,related_name="likes")
    pub_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "Tweet by {}".format(self.user.username)

class Retweet(models.Model):
    tweet = models.ForeignKey(Tweet,related_name="retweets",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='retweets', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User,related_name='comments', on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name="comments",on_delete=models.CASCADE)
