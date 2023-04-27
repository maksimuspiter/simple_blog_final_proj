from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from .models import Post, Comment
from .forms import CreateCommentAfterPost

from like_dislike.models import LikeDislike


def check_like_dislike(user, obj):
    obj_like_check = LikeDislike.objects.filter(
        content_type=ContentType.objects.get_for_model(obj),
        object_id=obj.pk,
        user=user,
    )
    if obj_like_check:
        obj_like_check = obj_like_check.first().vote
    else:
        obj_like_check = None
    return obj_like_check


def check_like_dislike_from_queryset(user, queryset):
    user_ckeck_comments_by_like_dislike = {}

    for query in queryset:
        query_like_check = check_like_dislike(user, query)
        if query_like_check:
            user_ckeck_comments_by_like_dislike[query.id] = query_like_check
    return user_ckeck_comments_by_like_dislike


def post_detail(request, *args, **kwargs):
    post = get_object_or_404(Post.published, slug=kwargs["slug"], pk=kwargs["pk"])
    comments = post.comments.all().filter(active=True)

    form = None
    post_like_check = None
    user_ckeck_comments_by_like_dislike = None

    if request.user.is_authenticated:
        post_like_check = check_like_dislike(request.user.portfolio, post)
        user_ckeck_comments_by_like_dislike = check_like_dislike_from_queryset(
            request.user.portfolio, comments
        )

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
        {
            "post": post,
            "comments": comments,
            "form": form,
            "post_like_check": post_like_check,
            "user_ckeck_comments_by_like_dislike": user_ckeck_comments_by_like_dislike,
        },
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ckeck_posts_by_like_dislike = None
        if self.request.user.is_authenticated:
            user_ckeck_posts_by_like_dislike = check_like_dislike_from_queryset(
                self.request.user.portfolio, self.get_queryset()
            )
        context["user_ckeck_posts_by_like_dislike"] = user_ckeck_posts_by_like_dislike
        return context


# TODO: add search by tags
# TODO: search by categories
# TODO: add related posts
# TODO: rating posts
# TODO: add authentication and authorization
