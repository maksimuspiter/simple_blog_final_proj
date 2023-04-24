from django.shortcuts import render
from .models import Post, Comment


def all_posts(request):
    posts = Post.objects.all()
    return render(request, "blog/post/list.html", {"posts": posts})
