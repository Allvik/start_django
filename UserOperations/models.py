from django.db import models


class My_user(models.Model):
    name = models.CharField(max_length=20, default="")
    password = models.CharField(max_length=20, default="")
    all_games = models.JSONField(default=[])
