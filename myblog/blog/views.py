from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse
from django.views.generic import ListView

from .models import Post, Comment
from .forms import CreateCommentAfterPost
from .check_like_dislike import check_like_dislike, check_like_dislike_from_queryset
from .update_raiting_fields import update_raiting_field


def update_all_posts_raiting(request):
    posts = Post.objects.all()
    answer = update_raiting_field(request, posts)
    return HttpResponse(answer)


def update_all_comments_raiting(request):
    comments = Comment.objects.all()
    answer = update_raiting_field(request, comments)
    return HttpResponse(answer)


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

        # Used union template (blog/post/includes/post_like_dislike.html)
        # for detail and list
        user_ckeck_posts_by_like_dislike = {post.pk: post_like_check}

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
            "user_ckeck_posts_by_like_dislike": user_ckeck_posts_by_like_dislike,
            "user_ckeck_comments_by_like_dislike": user_ckeck_comments_by_like_dislike,
        },
    )


class PostListView(ListView):
    paginate_by = 3
    template_name = "blog/post/list.html"
    context_object_name = "posts"

    def get_queryset(self, **kwargs):
        queriset = Post.objects.all()
        author = self.request.GET.get("author_nickname", None)
        category_slug = self.kwargs.get("category_slug", None)
        order = self.request.GET.get("order_by", None)

        if author:
            queriset = queriset.filter(author__nickname=author)
        if category_slug:
            queriset = queriset.filter(category__slug=category_slug)
        if order:
            match order:
                case "hot":
                    queriset = queriset.order_by("-updated", "-raiting")
                case "best":
                    print(queriset)
                    queriset = queriset.order_by("-raiting")
                case "new":
                    queriset = queriset.order_by("-updated")

        return queriset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ckeck_posts_by_like_dislike = None
        queriset = Post.objects.all()

        if self.request.user.is_authenticated:
            user_ckeck_posts_by_like_dislike = check_like_dislike_from_queryset(
                self.request.user.portfolio, self.get_queryset()
            )
        context["user_ckeck_posts_by_like_dislike"] = user_ckeck_posts_by_like_dislike
        return context


# TODO: add search by tags
# TODO: search by categories
# TODO: add related posts

# TODO: raiting must be in Redis test_url = nul
