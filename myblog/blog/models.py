from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from portfolio.models import UserPortfolio


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:posts-by-category", args=[self.slug])


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DR", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250, verbose_name="Заглавие")
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        UserPortfolio,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name="Автор поста",
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
    category = models.ForeignKey(
        Category, blank=True, null=True, related_name="posts", on_delete=models.SET_NULL
    )
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
                self.pk,
                self.slug,
            ],
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Пост"
    )
    author = models.ForeignKey(
        UserPortfolio,
        on_delete=models.CASCADE,
        related_name="blog_comments",
        verbose_name="Автор комментария",
    )
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
        return f"Комментарий {self.author.nickname} на пост {self.post}"


# class Raiting(models.Model):
#     user = models.ForeignKey(UserPortfolio, on_delete=models.CASCADE)


# TODO: add post_content_files ('text', 'video', 'image', 'file') Post <- Content
