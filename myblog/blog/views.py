from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from .models import Post, Comment, Category
from portfolio.forms import (
    CreateUserPortfolio,
    CreateUserPortfolio2,
    CreateCommentAfterPost,
)


def all_posts(request):
    posts = Post.objects.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, *args, **kwargs):
    post = get_object_or_404(Post.published, slug=kwargs["slug"], pk=kwargs["pk"])
    comments = post.comments.all().filter(active=True)
    form = None

    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateCommentAfterPost(request.POST)
            if form.is_valid():
                Comment.objects.create(
                    post=post,
                    author=request.user.portfolio,
                    body=form.cleaned_data["body"],
                )

        form = CreateCommentAfterPost()

    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


class PostListView(ListView):
    paginate_by = 2
    queryset = Post.published.all()
    template_name = "blog/post/list.html"
    context_object_name = "posts"


class PostListByPortfolioView(ListView):
    paginate_by = 2
    template_name = "blog/post/list.html"
    context_object_name = "posts"

    def get_queryset(self):
        author = self.kwargs["author_nickname"]
        return Post.published.filter(author__nickname=author)


class PostListByCategoryView(ListView):
    paginate_by = 2
    template_name = "blog/post/list.html"
    context_object_name = "posts"

    def get_queryset(self):
        category_slug = self.kwargs["category_slug"]
        return Post.published.filter(category__slug=category_slug)


# TODO: add search by tags
# TODO: search by categories
# TODO: add related posts
# TODO: rating posts
# TODO: add authentication and authorization
