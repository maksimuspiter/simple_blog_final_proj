from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from .models import Post, Comment
from .forms import CreateCommentAfterPost

from like_dislike.models import LikeDislike

# @require_http_methods(["POST"])
# @login_required
# def add_in_favorite(request, post_id):
#     favorite_post, created = FavoritePost.objects.get_or_create(user=request.user.portfolio, post_id=post_id)
#     next = request.POST.get('next')
#     return redirect(next)


def post_detail(request, *args, **kwargs):
    post = get_object_or_404(Post.published, slug=kwargs["slug"], pk=kwargs["pk"])
    post_like_check = None
    if post and request.user.is_authenticated:
        post_like_check = LikeDislike.objects.filter(
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.pk,
                user=request.user.portfolio,
            )
        if post_like_check:
            post_like_check = post_like_check.first().vote
        else:
            post_like_check = None
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
        {"post": post, "comments": comments, "form": form, 'post_like_check': post_like_check},
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
