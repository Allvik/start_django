# Generated by Django 3.2.4 on 2021-07-01 10:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='kol_users',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='game',
            name='next_round',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='game',
            name='round_start',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='time_start_round',
            field=models.DateField(default=datetime.date(2021, 7, 1)),
        ),
    ]
