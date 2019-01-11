from django import forms
from .models import Tweet,Tag
import re
from django.contrib.auth.models import User
from django.utils import timezone

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["content"]
        

    
    # def save(self,force_insert = False,force_update=False,commit = True):
    #     # get the new tweet by creating an instanc of the form
    #     tweet = super(TweetForm,self).save(commit = False) 
    #     #getting the content of the tweet
    #     content = self.cleaned_data["content"]
    #     # getting all the tags and removing the hash
    #     tags = re.findall("#\w+",content)
    #     tags_less_hash = [re.sub("#","",tag) for tag in tags]
    #     # set the id of the new tweet to the last one + 1

    #     ids = Tweet.objects.all().values_list("id",flat=True)
    #     tweet.id = max(ids) + 1

    #     # set the time to the current time
    #     tweet.pub_date = timezone.now()
    #     # set a default user for the tweet
    #     tweet.user = User.objects.first()
    #     # clear any likes for it to start with 0 likes
    #     tweet.likes.clear()
    #     tweet.tags.clear()
    #     tags_list = []
    #     # get_or_create a tag and add it to the tweets
    #     for tag in tags_less_hash:
    #         tag,created = Tag.objects.get_or_create(name = tag.lower())
            
    #     self.tags_helper.cleaned_data  = ".".join(tags_list)
    #     content = re.sub("#\w+","",content)

    #     tweet.content = content
    #     if commit:
    #         tweet.save()
    #     return tweet
