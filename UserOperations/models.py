from django.db import models


class My_user(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    all_games = []
