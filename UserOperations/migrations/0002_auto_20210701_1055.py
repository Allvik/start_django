# Generated by Django 3.2.4 on 2021-07-01 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserOperations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='my_user',
            name='cookie',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='my_user',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='my_user',
            name='password',
            field=models.CharField(default='', max_length=20),
        ),
    ]
