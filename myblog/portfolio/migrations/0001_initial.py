# Generated by Django 4.2 on 2023-04-25 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPortfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=255, unique=True, verbose_name='Никнейм')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('active', models.BooleanField(default=True, verbose_name='Активный')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'Портфолио',
                'verbose_name_plural': 'Портфолио',
                'ordering': ['created'],
            },
        ),
        migrations.AddIndex(
            model_name='userportfolio',
            index=models.Index(fields=['created'], name='portfolio_u_created_862508_idx'),
        ),
    ]
