from django.contrib import admin
from .models import UserPortfolio


@admin.register(UserPortfolio)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["nickname", "created", "user", "active"]
    list_filter = ["active", "created"]
    search_fields = ["nickname", "user"]
