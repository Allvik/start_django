# Generated by Django 3.2.4 on 2021-07-01 10:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0002_auto_20210701_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='time_start_round',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
