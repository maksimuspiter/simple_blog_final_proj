from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.all_posts, name="all-posts"),
]
