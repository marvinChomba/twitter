from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Retweet)
admin.site.register(Tweet)
admin.site.register(Comment)