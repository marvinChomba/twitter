from django.contrib import admin
from django.urls import path,include
from tweets import views

urlpatterns = [
    path("",include("tweets.urls")),
    path('admin/', admin.site.urls),
    path("auth/",include("authentication.urls")),

]
