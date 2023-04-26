from django.urls import path
from portfolio import views

app_name = "portfolio"

urlpatterns = [
    path(
        "create/",
        views.CreatePortfolioView.as_view(),
        name="portfolio-create",
    ),
    path("create2/", views.create_portfolio, name="portfolio-create2"),
    path("registration/", views.registration, name="registration"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("edit_portfolio/", views.edit_portfolio, name="edit-portfolio"),
    path("user_profile/", views.user_profile, name="my-profile"),
    path("user_profile/<str:nickname>/", views.user_profile, name="user-profile"),
]
