from django.shortcuts import render, redirect, get_object_or_404
from portfolio.forms import CreateUserPortfolio, CreateUserPortfolio2
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CreatePortfolioView(LoginRequiredMixin, CreateView):
    template_name = "blog/portfolio/create.html"
    form_class = CreateUserPortfolio
    # success_url = "blog:all-posts"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect("blog:all-posts")


def create_portfolio(request):
    if request.method == "POST":
        form = CreateUserPortfolio2(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            pass

    else:
        form = CreateUserPortfolio2()

    return render(request, "blog/portfolio/create.html", {"form": form})
