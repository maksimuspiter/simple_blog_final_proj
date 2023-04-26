import json

from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from .models import LikeDislike


# @require_http_methods(["POST"])
# @login_required
class VotesView(View):
    model = None  # Модель данных - Post или Comment
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                user=request.user.portfolio,
            )
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=["vote"])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user.portfolio, vote=self.vote_type)
            result = True

        # return HttpResponse(
        #     json.dumps(
        #         {
        #             "result": result,
        #             "like_count": obj.votes.likes().count(),
        #             "dislike_count": obj.votes.dislikes().count(),
        #             "sum_rating": obj.votes.sum_rating(),
        #         }
        #     ),
        #     content_type="application/json",
        # )
        next = request.POST.get("next", "/")
        return redirect(next)


"""
return redirect(request.META.get('HTTP_REFERER'))


<form method="POST">
    {% csrf_token %}
    {{ form }}
    <input type="hidden" name="next" value="{{ request.path }}">
    <button type="submit">Let's Go</button>
</form>
"""
