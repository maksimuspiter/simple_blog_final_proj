from .models import UserPortfolio
from django.forms import ModelForm
from django import forms


class CreateUserPortfolio(ModelForm):
    class Meta:
        model = UserPortfolio
        # fields = ["user", "nickname"]
        fields = ["nickname"]


class CreateUserPortfolio2(forms.Form):
    nickname = forms.CharField(max_length=20, label="Никнейм", 
                               label_suffix='exampleFormControlInput1')
