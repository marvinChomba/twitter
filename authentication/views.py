from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Welcome")
    else:
        form = UserCreationForm()

    context = {
        "form":form
    }

    return render(request,"registration/registration_form.html",context)

def profile(request,id):
    user = User.objects.get(id = id)
    # user.select_related("profile","tweets","retweets").prefetch_related("likes")
    return render(request,"user/profile.html",locals())