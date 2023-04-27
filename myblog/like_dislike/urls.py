from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from .models import LikeDislike
from blog.models import Post, Comment

app_name = "like_dislike"

urlpatterns = [
    path(
        "post/<int:pk>/like/",
        login_required(views.VotesView.as_view(model=Post, vote_type=LikeDislike.LIKE)),
        name="post_like",
    ),
    path(
        "post/<int:pk>/dislike/",
        login_required(
            views.VotesView.as_view(model=Post, vote_type=LikeDislike.DISLIKE)
        ),
        name="post_dislike",
    ),
    path(
        "comment/<int:pk>/like/",
        login_required(
            views.VotesView.as_view(model=Comment, vote_type=LikeDislike.LIKE)
        ),
        name="comment_like",
    ),
    path(
        "comment/<int:pk>/dislike/",
        login_required(
            views.VotesView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE)
        ),
        name="comment_dislike",
    ),
]
