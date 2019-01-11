from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Retweet)
@admin.register(Tweet)

class TweetAdmin(admin.ModelAdmin):
    list_display = ("id","content","user")

    
admin.site.register(Comment)
admin.site.register(Tag)
