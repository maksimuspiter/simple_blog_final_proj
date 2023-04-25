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
]
