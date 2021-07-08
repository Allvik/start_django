import django.http
from django.http import HttpResponseRedirect
from django.shortcuts import render
from UserOperations.models import My_user
from Game.models import Game
import random
import urllib.parse


def index(request):
    return render(request, "index.html")


def registration(request):
    if request.method != "POST" or "name" not in request.POST or "password" not in request.POST or \
            len(My_user.objects.filter(name=urllib.parse.quote_plus(request.POST["name"]))) != 0:
        return django.http.HttpResponse(status=404)
    current_user = My_user(name=urllib.parse.unquote_plus(request.POST["name"]),
                           password=urllib.parse.unquote_plus(request.POST["password"]),
                           cookie=random.randint(1, 10**9))
    current_user.save()
    response = HttpResponseRedirect('/yourCabinet')
    response.set_cookie("hat", current_user.cookie)
    return response


def login(request):
    if request.method != "POST" or "name" not in request.POST or "password" not in request.POST:
        return django.http.HttpResponse(status=404)
    current_user = My_user.objects.filter(name=urllib.parse.unquote_plus(request.POST["name"]),
                                          password=urllib.parse.unquote_plus(request.POST["password"]))
    if len(current_user) == 0:
        return django.http.HttpResponse(status=404)
    current_user = current_user[0]
    response = HttpResponseRedirect('/yourCabinet')
    response.set_cookie("hat", current_user.cookie)
    return response


def getCabinet(request):
    if request.method != "GET" or "hat" not in request.COOKIES:
        return django.http.HttpResponse(status=404)
    cur_user = My_user.objects.filter(cookie=request.COOKIES["hat"])[0]
    all_games = []
    for i in cur_user.all_games:
        all_games.append(Game.objects.filter(id=i)[0])
    return render(request, "yourCabinet.html", {'games': all_games})


def debug_base(request):
    print("Users:", list(My_user.objects.all()))
    print("Games:", list(Game.objects.all()))
    print("Cookies: ", list(request.COOKIES))
    return django.http.HttpResponse(status=404)


def clear_bases(request):
    for object_user in My_user.objects.all():
        object_user.delete()
    for object_game in Game.objects.all():
        object_game.delete()
    return django.http.HttpResponse(status=404)

