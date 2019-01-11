from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),
    path("like/",views.like,name="like"),
    path("add/tweet/",views.add_tweet,name="add_tweet")
]