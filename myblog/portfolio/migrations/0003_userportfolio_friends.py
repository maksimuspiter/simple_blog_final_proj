# Generated by Django 4.2 on 2023-04-26 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_userportfolio_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='userportfolio',
            name='friends',
            field=models.ManyToManyField(to='portfolio.userportfolio', verbose_name='Друзья'),
        ),
    ]
