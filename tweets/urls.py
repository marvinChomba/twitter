from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("like/",views.like,name="like"),
    path("add/tweet/",views.add_tweet,name="add_tweet"),
    path("retweet/",views.retweet,name="retweet"),
    path("add/comment/",views.add_comment,name="add_comment"),
    path("tweet/<int:tweet_id>/",views.single_tweet,name = "single_tweet"),
    path("search/",views.search,name="search")
]