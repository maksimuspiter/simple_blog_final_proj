from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import UserPortfolio


class CreateUserPortfolio(ModelForm):
    class Meta:
        model = UserPortfolio
        # fields = ["user", "nickname"]
        fields = ["nickname"]


class CreateUserPortfolio2(forms.Form):
    nickname = forms.CharField(
        max_length=20, label="Никнейм", label_suffix="exampleFormControlInput1"
    )


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя или никнейм")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class UserRegistrationForm(forms.ModelForm):
    nickname = forms.CharField(max_length=255, label="Никнейм")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "nickname"]
        labels = {
            "username": "Имя пользователя",
            "first_name": "Имя",
            "email": "Почта",
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Пароли не совпадают.")
        if len(cd["password"]) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов")

        return cd["password2"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Этот почтовый адрес уже используется.")
        return data

    def clean_nickname(self):
        data = self.cleaned_data["nickname"]
        if UserPortfolio.objects.filter(nickname=data).exists():
            raise forms.ValidationError("Этот никнейм уже занят.")
        return data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        data = self.cleaned_data["email"]
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email already in use.")
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserPortfolio
        fields = ["nickname"]

    def clean_nickname(self):
        data = self.cleaned_data["nickname"]
        qs = UserPortfolio.objects.exclude(id=self.instance.id).filter(nickname=data)
        if qs.exists():
            raise forms.ValidationError("Этот никнейм уже занят.")
        return data
