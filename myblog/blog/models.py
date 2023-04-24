from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DR", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250, verbose_name="Заглавие")
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        "UserPortfolio",
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name="Автор",
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="статус",
    )
    # manager
    objects = models.Manager()
    published = PublishedManager()
    # ManyToMany taggit
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:single-post",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост"
    )
    name = models.CharField(max_length=80, verbose_name="Название")
    email = models.EmailField()
    body = models.TextField(verbose_name="Контент")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")
    active = models.BooleanField(default=True, verbose_name="Активный")

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий {self.name} на пост {self.post}"


class UserPortfolio(models.Model):
    user = models.ForeignKey(
        User, related_name="portfolios", verbose_name="автор", on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=255, unique=True, verbose_name="Никнейм")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    active = models.BooleanField(default=True, verbose_name="Активный")

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]
        verbose_name = "Портфолио"
        verbose_name_plural = "Портфолио"

    def __str__(self):
        return f"Никнейм {self.nickname}, user_id {self.user.pk}"

#TODO: add categories 
#TODO: add post_content_files ('text', 'video', 'image', 'file') Post <- Content 