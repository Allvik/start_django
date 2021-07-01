from django.shortcuts import render
from UserOperations.models import My_user
from Game.models import Game
import random


def index(request):
    return render(request, "index.html")


def registration(request):
    if request.method != "POST":
        return
    if "name" not in request.POST or "password" not in request.POST:
        return
    user_with_eq_login = My_user.objects.filter(name=request.POST["name"])
    if user_with_eq_login is not None:
        return
    current_user = My_user(name=request.POST["name"], password=request.POST["password"],
                                  cookie=random.randint(1, 10**9))
    current_user.save()
    response = render(request, "yourCabinet.html")
    response.set_cookie("hat", current_user.cookie)
    return response


def login(request):
    if request.method != "POST":
        return
    if "name" not in request.POST or "password" not in request.POST:
        return
    current_user = My_user.objects.filter(name=request.POST["name"], password=request.POST["password"])
    if current_user is None:
        return
    current_user = current_user[0]
    response = render(request, "yourCabinet.html")
    response.set_cookie("hat", current_user.cookie)
    return response


def create_game(request):
    if request.method != "POST":
        return
    if "name" not in request.POST or "password" not in request.POST or "countPlayers" not in request.POST or "hat" not in request.COOKIES:
        return



def debug_base(request):
    print("Users:", list(My_user.objects.all()))
    print("Games:", list(Game.objects.all()))


def clear_bases(request):
    for object_user in My_user.objects.all():
        object_user.delete()
    for object_game in Game.objects.all():
        object_game.delete()
