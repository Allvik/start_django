import datetime

import django.utils.timezone
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=20, default="")
    password = models.CharField(max_length=20, default="")
    all_users = models.JSONField(default=[])
    all_words = models.JSONField(default=[])
    all_remaining_words = models.JSONField(default=[])
    kol_users = models.IntegerField(default=0)
    next_round = models.IntegerField(default=0)
    number_word = models.IntegerField(default=0)
    round_start = models.BooleanField(default=False)
    game_end = models.BooleanField(default=False)
    time_start_round = models.DateTimeField(default=datetime.datetime.today())
