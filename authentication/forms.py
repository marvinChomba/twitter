from django import forms
from django.contrib.auth.models import User

class RegForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name","email"]


    def clean_email(self):
        if User.objects.filter(email = self.cleaned_data["email"]):
            raise forms.ValidationError("Email already in use")
        else:
            return self.cleaned_data["email"]
