from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Comment


def all_posts(request):
    posts = Post.objects.all()
    return render(request, "blog/post/list.html", {"posts": posts})


class PostListView(ListView):
    paginate_by = 1
    model = Post
    template_name = "blog/post/list.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post/detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["info"] = "hello world"
        return context
