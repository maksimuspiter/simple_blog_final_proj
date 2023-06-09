from django.contrib import admin
from .models import LikeDislike


@admin.register(LikeDislike)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["vote", "user", "content_type", "object_id"]
