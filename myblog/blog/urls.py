from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="all-posts"),
    path(
        "posts/<str:author_nickname>",
        views.PostListView.as_view(),
        name="posts-by-author",
    ),
    path(
        "posts/category/<str:category_slug>",
        views.PostListView.as_view(),
        name="posts-by-category",
    ),
    path(
        "post/<int:year>/<int:month>/<int:day>/<int:pk>/<slug:slug>/",
        views.post_detail,
        name="single-post",
    ),
    path(
        "update_all_posts_raiting/", views.update_all_posts_raiting, name="update_all_posts_raiting"
    ),
    path(
        "update_all_comments_raiting/",
        views.update_all_comments_raiting,
        name="update_all_comments_raiting",
    ),
]
