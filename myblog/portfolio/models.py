from django.db import models
from django.contrib.auth.models import User


class UserPortfolio(models.Model):
    user = models.OneToOneField(
        User, related_name="portfolio", verbose_name="автор", on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=255, unique=True, verbose_name="Никнейм")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    active = models.BooleanField(default=True, verbose_name="Активный")
    avatar = models.ImageField(upload_to='users/avatar/%Y/%m/%d/',
                              blank=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
        verbose_name = "Портфолио"
        verbose_name_plural = "Портфолио"

    def __str__(self):
        return f"Никнейм {self.nickname}, user_id {self.user.pk}"