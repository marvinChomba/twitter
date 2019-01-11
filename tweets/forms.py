from django import forms
from .models import Tweet,Tag
import re
from django.contrib.auth.models import User
from django.utils import timezone

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["content"]

    def clean_content(self):
        if len(self.cleaned_data["content"]) > 140:
            raise forms.ValidationError("Maximum character length is 140 bro")
        return self.cleaned_data["content"]

    

