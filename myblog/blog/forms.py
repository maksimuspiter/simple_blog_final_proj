from .models import UserPortfolio
from django.forms import ModelForm
from django import forms


class CreateUserPortfolio(ModelForm):
    class Meta:
        model = UserPortfolio
        # fields = ["user", "nickname"]
        fields = ["nickname"]

