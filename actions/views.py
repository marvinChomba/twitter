from django.shortcuts import render
from .models import Action

# Create your views here.
def notifications(request):
    user_ids = request.user.profile.following.all().values_list("id",flat = True)
    print(user_ids)

    actions = Action.objects.filter(user_id__in = user_ids).order_by("-time")

    context = {
        "actions":actions,
        "section":"notifs"
    }

    return render(request,"actions.html",context)