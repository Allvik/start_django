# Generated by Django 3.2.4 on 2021-07-09 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0006_auto_20210708_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='cookie',
        ),
    ]
