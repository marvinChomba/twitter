from django.shortcuts import render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from tweets.models import *
from .forms import RegForm
from actions.utils import add_action

# Create your views here.
def register(request):
    if request.method == "POST":
        form1 = RegForm(request.POST)
        form2 = UserCreationForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form2.save(commit = False)
            user.first_name = form1.cleaned_data["first_name"]
            user.last_name = form1.cleaned_data["last_name"]
            user.email = form1.cleaned_data["email"]
            user.save()
            return HttpResponse("Welcome")
    else:
        form1 = RegForm()
        form2 = UserCreationForm()

    context = {
        "form1":form1,
        'form2':form2
    }

    return render(request,"registration/registration_form.html",context)


def profile(request,user_id):
    # if user_id == request.id:
        # return redirect("my_profile")
    user = User.objects.get(id = user_id)
    tweets = Tweet.objects.filter(user_id = user_id)
    rewtweets = Retweet.objects.filter(user_id = user_id)
    all_tweets = []
    for tweet in tweets:
        all_tweets.append(tweet)
    for rewtweet in rewtweets:
        all_tweets.append(rewtweet)
    
    all_tweets.sort(key = lambda u: u.pub_date,reverse = True)

    return render(request,"user/profile.html",{"user":user,"tweets":all_tweets})

def follow_user(request):
    user_id = request.POST.get("id")
    user = get_object_or_404(User,id=int(user_id))

    if request.user in user.profile.followers.all():
        user.profile.followers.remove(request.user)
        request.user.profile.following.remove(user)
        has_followed = False
    else:
        user.profile.followers.add(request.user)
        request.user.profile.following.add(user)
        has_followed = True

    
    data = {
        "has_followed":has_followed,
        "count":user.profile.followers.all().count()
    }

    add_action(user = request.user,target = user, action= "followed")

    return JsonResponse(data)

