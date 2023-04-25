from django.forms import ModelForm

from .models import Comment


class CreateCommentAfterPost(ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
