from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Tweet(models.Model):
    user = models.ForeignKey(User,related_name='tweets',on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User,related_name="likes",blank=True)
    pub_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    tags = models.ManyToManyField(Tag,related_name = "tags",blank=True)
    tags_helper = models.CharField(max_length = 400,blank=True)

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return "Tweet by {}".format(self.user.username)

class Retweet(models.Model):
    tweet = models.ForeignKey(Tweet,related_name="retweets",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name = "retweets", on_delete = models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    is_retweet = models.BooleanField(default = True)


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User,related_name='comments', on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name="comments",on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add =True,blank=True,null=True)

    class Meta:
        ordering = ["-pub_date"]
    


