from django.shortcuts import render
from . import models


def index(request):
    all_objects = list(models.My_user.objects.filter(name="f"))
    print(all_objects[0].id)
    return render(request, "index.html")


def registration(request):
    if request.method != "POST":
        return
    print(request.POST)
    if "name" not in request.POST or "password" not in request.POST:
        return
    current_user = models.My_user(name=request.POST["name"], password=request.POST["password"])
    current_user.save()
    return render(request, "index.html")

