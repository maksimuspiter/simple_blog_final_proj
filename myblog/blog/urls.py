from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    # path("", views.all_posts, name="all-posts"),
    path("", views.PostListView.as_view(), name="all-posts"),
    # path("post/<int:pk>/<slug:slug>/", views.PostDetailView.as_view(), name="single-post"),
    # path(
    #     "post/<int:year>/<int:month>/<int:day>/<int:pk>/<slug:slug>/",
    #     views.PostDetailView.as_view(),
    #     name="single-post",
    # ),
    path(
        "post/<int:year>/<int:month>/<int:day>/<int:pk>/<slug:slug>/",
        views.post_detail,
        name="single-post",
    ),
    path(
        "posts/<str:author_nickname>",
        views.PostListByPortfolioView.as_view(),
        name="posts-by-author",
    ),
    path(
        "portfolio/create/",
        views.CreatePortfolioView.as_view(),
        name="portfolio-create",
    ),
    path("portfolio/create2/", views.create_portfolio, name="portfolio-create2"),
]
