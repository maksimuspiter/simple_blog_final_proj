from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from .models import Post, Comment, FavoritePost
from .forms import CreateCommentAfterPost


def add_in_favorite(request, post_id):
    FavoritePost.objects.create(user=request.user, post__id=post_id)


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
    template_name = "blog/post/list.html"
    context_object_name = "posts"

    def get_queryset(self):
        author = self.kwargs.get("author_nickname", None)
        if author:
            return Post.published.filter(author__nickname=author)
        category_slug = self.kwargs.get("category_slug", None)
        if category_slug:
            return Post.published.filter(category__slug=category_slug)

        return Post.published.all()


# TODO: add search by tags
# TODO: search by categories
# TODO: add related posts
# TODO: rating posts
# TODO: add authentication and authorization
