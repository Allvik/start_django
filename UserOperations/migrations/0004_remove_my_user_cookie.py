# Generated by Django 3.2.4 on 2021-07-09 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserOperations', '0003_my_user_all_games'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='my_user',
            name='cookie',
        ),
    ]