# Generated by Django 4.2 on 2023-04-25 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userportfolio',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='users/avatar/%Y/%m/%d/'),
        ),
    ]
