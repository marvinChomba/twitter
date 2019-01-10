from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

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