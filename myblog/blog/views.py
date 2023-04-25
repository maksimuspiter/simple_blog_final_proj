from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment, UserPortfolio
from .forms import CreateUserPortfolio, CreateUserPortfolio2


def all_posts(request):
    posts = Post.objects.all()
    return render(request, "blog/post/list.html", {"posts": posts})


class PostListView(ListView):
    paginate_by = 2
    queryset = Post.published.all()
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


class PostListByPortfolioView(ListView):
    paginate_by = 2
    template_name = "blog/post/list.html"
    context_object_name = "posts"

    # queryset = Post.published.filter

    def get_queryset(self):
        author = self.kwargs["author_nickname"]
        return Post.published.filter(author__nickname=author)


class CreatePortfolioView(LoginRequiredMixin, CreateView):
    template_name = "blog/portfolio/create.html"
    form_class = CreateUserPortfolio
    # success_url = "blog:all-posts"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect('blog:all-posts')

    # def get(self, request, *args, **kwargs):
    #     context = {'form': CreateUserPortfolio}
    #     return render(request, 'blog/portfolio/create.html', context)

    # def post(self, request, *args, **kwargs):
    #     form = CreateUserPortfolio(request.POST)
    #     #if form.is_valid():
    #         #portfolio = form.save(commit=False)
    #     print(form.cleaned_data)
    #         # return reverse('blog:all-posts')
    #     return render(request, 'blog/portfolio/create.html', {'form': form})

def create_portfolio(request):
    if request.method == 'POST':
        form = CreateUserPortfolio2(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            
    else:
        form = CreateUserPortfolio2()
    
    return render(request, 'blog/portfolio/create.html', {'form': form})

# TODO: add search by tags
# TODO: search by categories
# TODO: add comments after detail post
# TODO: add related posts
# TODO: rating posts
