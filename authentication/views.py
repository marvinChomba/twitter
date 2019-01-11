from django.shortcuts import render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse,JsonResponse
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

    return JsonResponse(data)

