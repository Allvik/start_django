import django.http
from django.http import HttpResponseRedirect
from django.shortcuts import render
from UserOperations.models import My_user
from Game.models import Game
import random
import urllib.parse

# Create your views here.


def createGame(request):
    if request.method != "POST" or "name" not in request.POST or "password" not in request.POST or \
            "countPlayers" not in request.POST or \
            "hat" not in request.COOKIES or int(request.POST["countPlayers"]) % 2 == 1 \
            or int(request.POST["countPlayers"]) <= 0 or len(Game.objects.filter(name=request.POST["name"])) != 0:
        return django.http.HttpResponse(status=404)
    cur_user = My_user.objects.filter(cookie=request.COOKIES["hat"])[0]
    new_game = Game(name=urllib.parse.unquote_plus(request.POST["name"]),
                    password=urllib.parse.unquote_plus(request.POST["password"]),
                    kol_users=int(request.POST["countPlayers"]), cookie=random.randint(1, 10**9))
    new_game.all_users.append([cur_user.id, 0, False])
    new_game.save()
    cur_user.all_games.append(new_game.id)
    cur_user.save()
    return HttpResponseRedirect('/yourCabinet')


def enterGame(request):
    if request.method != "POST" or "name" not in request.POST or "password" not in request.POST or \
            "hat" not in request.COOKIES:
        return django.http.HttpResponse(status=404)
    cur_game = Game.objects.filter(name=urllib.parse.unquote_plus(request.POST["name"]),
                                   password=urllib.parse.unquote_plus(request.POST["password"]))
    if len(cur_game) == 0:
        return django.http.HttpResponse(status=404)
    cur_game = cur_game[0]
    cur_user = My_user.objects.filter(cookie=request.COOKIES["hat"])[0]
    if cur_game.kol_users == len(cur_game.all_users):
        return django.http.HttpResponse(statis=404)
    for i in cur_user.all_games:
        if Game.objects.filter(id=i)[0].name == request.POST["name"]:
            return django.http.HttpResponse(status=404)
    cur_user.all_games.append(cur_game.id)
    cur_game.all_users.append([cur_user.id, 0, False])
    cur_user.save()
    cur_game.save()
    return HttpResponseRedirect('/yourCabinet')


def play(request):
    if request.method != "POST" or "id" not in request.POST or "hat" not in request.COOKIES:
        return django.http.HttpResponse(status=404)
    cur_user = My_user.objects.filter(cookie=request.POST["hat"])
    if len(cur_user) == 0:
        return django.http.HttpResponse(status=404)
    cur_user = cur_user[0]
    for i in cur_user.all_games:
        if i[0] == request.POST["id"]:
            if i[2] is False:
                response = render(request, "makeWords.html")
                response.set_cookie("game", Game.objects.filter(id=request.POST["id"])[0].cookie)
                return response
            else:
                #add gameplay
                pass
    return django.http.HttpResponse(status=404)


def makeWords(request):
    if request.method != "POST" or "hat" not in request.COOKIES or "game" not in request.COOKIES:
        return django.http.HttpResponse(status=404)
    for i in range(1, 6):
        if f"word{i}" not in request.POST:
            return django.http.HttpResponse(status=404)
    cur_user = My_user.objects.filter(cookie=request.COOKIES["hat"])
    for i in cur_user.all_games:
        pass
