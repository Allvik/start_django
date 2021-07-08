import django.utils.timezone
from django.db import models


class Game(models.Model):
    cookie = models.IntegerField(default=0)
    name = models.CharField(max_length=20, default="")
    password = models.CharField(max_length=20, default="")
    all_users = models.JSONField(default=[])
    all_words = models.JSONField(default=[])
    kol_users = models.IntegerField(default=0)
    next_round = models.IntegerField(default=1)
    round_start = models.BooleanField(default=False)
    time_start_round = models.DateField(default=django.utils.timezone.now)
