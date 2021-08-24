import datetime

import django.http
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from UserOperations.models import My_user
from Game.models import Game
import random
import urllib.parse


def createGame(request):
    if request.method != "POST" or "name" not in request.POST or "password" not in request.POST or \
            "countPlayers" not in request.POST or \
            "user" not in request.COOKIES or int(request.POST["countPlayers"]) % 2 == 1 \
            or int(request.POST["countPlayers"]) <= 0 or \
            len(Game.objects.filter(name=urllib.parse.unquote_plus(request.POST["name"]))) != 0:
        return HttpResponse("У вас нет кук или не все поля есть или поля неккоректны")
    cur_user = My_user.objects.filter(id=request.COOKIES["user"])[0]
    new_game = Game(name=urllib.parse.unquote_plus(request.POST["name"]),
                    password=urllib.parse.unquote_plus(request.POST["password"]),
                    kol_users=int(request.POST["countPlayers"]))
    new_game.all_users.append([cur_user.id, 0, False])
    new_game.save()
    cur_user.all_games.append(new_game.id)
    cur_user.save()
    return HttpResponseRedirect('/yourCabinet')


def enterGame(request):
    if request.method != "POST" or "name" not in request.POST or "password" not in request.POST or \
            "user" not in request.COOKIES:
        return HttpResponse("У вас нет кук или не все поля есть")
    cur_game = Game.objects.filter(name=urllib.parse.unquote_plus(request.POST["name"]),
                                   password=urllib.parse.unquote_plus(request.POST["password"]))
    if len(cur_game) == 0:
        return HttpResponse("Такой игры не существует")
    cur_game = cur_game[0]
    cur_user = My_user.objects.filter(id=request.COOKIES["user"])[0]
    if cur_game.kol_users == len(cur_game.all_users):
        return HttpResponse("В игре не осталось места")
    for i in cur_user.all_games:
        if Game.objects.filter(id=i)[0].name == request.POST["name"]:
            return HttpResponse("Вы уже вошли в эту игру ранее")
    cur_user.all_games.append(cur_game.id)
    cur_game.all_users.append([cur_user.id, 0, False])
    cur_user.save()
    cur_game.save()
    return HttpResponseRedirect('/yourCabinet')


def play(request):
    if "user" not in request.COOKIES or \
            ((request.method != "POST" or "id" not in request.POST) and
             (request.method != "GET" or "game" not in request.COOKIES)):
        return HttpResponse("У вас нет кук или не все поля есть")
    cur_user = My_user.objects.filter(id=request.COOKIES["user"])[0]
    cur_game = None
    if "id" in request.POST:
        game_id = int(request.POST["id"])
    else:
        game_id = int(request.COOKIES["game"])
    for i in cur_user.all_games:
        if i == game_id:
            cur_game = Game.objects.filter(id=i)[0]
            break
    if cur_game is None:
        return HttpResponse("У вас нет такой игры")
    for i in cur_game.all_users:
        if i[0] == cur_user.id:
            if i[2] is False:
                response = render(request, "makeWords.html")
                response.set_cookie("game", cur_game.id)
                return response
            break
    if len(cur_game.all_users) < cur_game.kol_users:
        return HttpResponse("Не все пользователи зашли в игру")
    if len(cur_game.all_words) < 5 * cur_game.kol_users:
        return HttpResponse("Не все пользователи придумали слова")
    updateGame(cur_game)
    change = ((2 * cur_game.next_round // cur_game.kol_users) & 1)
    person1 = cur_game.all_users[((2 * cur_game.next_round) % cur_game.kol_users) ^ change][0]
    person2 = cur_game.all_users[((2 * cur_game.next_round) % cur_game.kol_users + 1) ^ change][0]
    response = render(request, "game.html", {"move1": (person1 == cur_user.id), "move2": (person2 == cur_user.id),
                                         "started": cur_game.round_start,
                                         "word": cur_game.all_words[cur_game.number_word],
                                         "game_end": cur_game.game_end})
    response.set_cookie("game", cur_game.id)
    return response


def makeWords(request):
    if request.method != "POST" or "user" not in request.COOKIES or "game" not in request.COOKIES:
        return HttpResponse("У вас нет кук или не все поля есть")
    for i in range(1, 6):
        if f"word{i}" not in request.POST:
            return HttpResponse("У вас нет кук или не все поля есть")
    cur_user = My_user.objects.filter(id=request.COOKIES["user"])[0]
    cur_game = None
    for i in cur_user.all_games:
        if i == int(request.COOKIES["game"]):
            cur_game = Game.objects.filter(id=i)[0]
            break
    if cur_game is None:
        return HttpResponse("У вас нет такой игры")
    for i in range(len(cur_game.all_users)):
        if cur_game.all_users[i][0] == cur_user.id:
            if cur_game.all_users[i][2] is False:
                for j in range(1, 6):
                    cur_game.all_words.append(urllib.parse.unquote_plus(request.POST[f"word{j}"]))
                    cur_game.all_remaining_words.append(True)
                cur_game.all_users[i][2] = True
                cur_game.save()
                return HttpResponseRedirect('/play')
            return HttpResponse("Вы уже ввели свои слова")
    return HttpResponse("Что-то пошло не так")


def updateGame(game):
    if game.round_start:
        now = datetime.datetime.today()
        if now.timestamp() - game.time_start_round.timestamp() > 30:
            game.next_round += 1
            game.round_start = False
    game_end = True
    for i in game.all_remaining_words:
        if i is True:
            game_end = False
    game.game_end = game_end
    game.save()


def next_word(game):
    if game.game_end is True:
        return
    kol_words = 0
    for i in game.all_remaining_words:
        if i is True:
            kol_words += 1
    number_word = random.randint(0, kol_words - 1)
    kol_words = 0
    for i in range(game.kol_users * 5):
        if game.all_remaining_words[i] is True:
            kol_words += 1
        if kol_words == number_word + 1:
            game.number_word = i
            break
    game.save()


def start_round(request):
    if "user" not in request.COOKIES or "game" not in request.COOKIES:
        return HttpResponse("У вас нет какой-то куки")
    cur_game = Game.objects.filter(id=request.COOKIES["game"])[0]
    updateGame(cur_game)
    if cur_game.round_start:
        return HttpResponse("Предыдущий раунд еще не закончился")
    person1 = cur_game.all_users[(cur_game.next_round * 2) % cur_game.kol_users + ((cur_game.next_round * 2) //
                                 cur_game.kol_users) % 2][0]
    if person1 == int(request.COOKIES["user"]):
        next_word(cur_game)
        cur_game.round_start = True
        cur_game.time_start_round = datetime.datetime.today()
        cur_game.save()
        return HttpResponseRedirect('/play')
    return HttpResponse("Вы не отгадываете в этом раунде")


def yesWord(request):
    if "user" not in request.COOKIES or "game" not in request.COOKIES:
        return HttpResponse("У вас нет куки")
    cur_game = Game.objects.filter(id=request.COOKIES["game"])[0]
    updateGame(cur_game)
    if cur_game.round_start is False:
        return HttpResponse("Раунд кончился, вы не успели")
    num1 = (cur_game.next_round * 2) % cur_game.kol_users + ((cur_game.next_round * 2) // cur_game.kol_users) % 2
    print(num1)
    person1 = cur_game.all_users[num1][0]
    if person1 == int(request.COOKIES["user"]):
        cur_game.all_remaining_words[cur_game.number_word] = False
        cur_game.all_users[num1][1] += 1
        cur_game.all_users[num1 ^ 1][1] += 1
        print(cur_game.all_users[num1][1])
        cur_game.save()
        updateGame(cur_game)
        next_word(cur_game)
        return HttpResponseRedirect('/play')
    return HttpResponse("Не вы отгадываете")


def noWord(request):
    if "user" not in request.COOKIES or "game" not in request.COOKIES:
        return HttpResponse("У вас нет куки")
    cur_game = Game.objects.filter(id=request.COOKIES["game"])[0]
    updateGame(cur_game)
    if cur_game.round_start is False:
        return HttpResponse("Раунд кончился, вы не успели")
    person1 = cur_game.all_users[(cur_game.next_round * 2) % cur_game.kol_users + ((cur_game.next_round * 2) //
                                 cur_game.kol_users) % 2][0]
    if person1 == int(request.COOKIES["user"]):
        updateGame(cur_game)
        next_word(cur_game)
        return HttpResponseRedirect('/play')
    return HttpResponse("Не вы отгадываете")


class person_for_standings():
    points = 0
    name = ""

    def __init__(self, _points, _name):
        self.points = _points
        self.name = _name


def getStandings(request):
    if "user" not in request.COOKIES or "game" not in request.COOKIES or request.method != "GET":
        return HttpResponse("У вас нет куки")
    cur_game = Game.objects.filter(id=request.COOKIES["game"])[0]
    there_is_user = False
    for i in cur_game.all_users:
        if i[0] == int(request.COOKIES["user"]):
            there_is_user = True
            break
    if not there_is_user:
        return HttpResponse("У вас нет такой игры")
    all_users = []
    for i in cur_game.all_users:
        all_users.append(person_for_standings(i[1], My_user.objects.filter(id=i[0])[0].name))
    all_users.sort(key=lambda x: -x.points)
    print(all_users[1].name, all_users[1].points)
    return render(request, "standings.html", {"all_users": all_users})
