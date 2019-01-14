from django.urls import path
from . import views

urlpatterns = [
    path("actions/",views.notifications,name="notifs")
]