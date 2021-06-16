from django.db import models


class User(models.Model):
    nickname = models.CharField(max_length=20)
    cookie = models.CharField(max_length=10)


#User.objects.filter(nickname="Lesha").all()