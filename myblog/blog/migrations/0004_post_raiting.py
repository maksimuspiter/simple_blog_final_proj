# Generated by Django 4.2 on 2023-04-27 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_post_likes_delete_favoritepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='raiting',
            field=models.BigIntegerField(default=0),
        ),
    ]