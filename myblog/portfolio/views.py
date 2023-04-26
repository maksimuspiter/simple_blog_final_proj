from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from portfolio.forms import CreateUserPortfolio, CreateUserPortfolio2
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from .models import UserPortfolio
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from blog.models import Post


class CreatePortfolioView(LoginRequiredMixin, CreateView):
    template_name = "portfolio/create.html"
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
            pass

    else:
        form = CreateUserPortfolio2()

    return render(request, "portfolio/create.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(
                        request, messages.SUCCESS, f"Добро пожаловать.{user.portfolio}"
                    )
                    return redirect("blog:all-posts")

                else:
                    return HttpResponse("Ваш аккаунт не активен")
            else:
                messages.add_message(request, messages.SUCCESS, f"Invalid login")
    else:
        form = LoginForm()
    return render(request, "portfolio/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("blog:all-posts")


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            # Create the user profile
            nickname = form.cleaned_data["nickname"]

            UserPortfolio.objects.create(user=new_user, nickname=nickname)
            return render(
                request, "portfolio/register_done.html", {"new_user": new_user}
            )

    else:
        form = UserRegistrationForm()
    return render(request, "portfolio/register.html", {"form": form})


def user_profile(request, nickname=None):
    if not nickname:
        author = get_object_or_404(UserPortfolio, user=request.user)
    else:
        author = get_object_or_404(UserPortfolio, nickname=nickname, active=True)

    posts = Post.published.filter(author=author)

    return render(
        request, "portfolio/user_profiles.html", {"author": author, "posts": posts}
    )
