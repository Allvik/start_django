# Generated by Django 3.2.4 on 2021-07-07 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0004_game_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='cookie',
            field=models.IntegerField(default=0),
        ),
    ]
