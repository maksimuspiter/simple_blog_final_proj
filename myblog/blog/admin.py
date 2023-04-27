from django.contrib import admin
from .models import Post, Comment, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "author",
        "publish",
        "status",
        "category",
        "raiting",
    ]
    list_filter = ["status", "created", "publish", "author", "category"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish", "category"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name", "slug"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "post", "created", "active", "raiting"]
    list_filter = ["author", "active", "created", "updated"]
    search_fields = ["author", "body"]
