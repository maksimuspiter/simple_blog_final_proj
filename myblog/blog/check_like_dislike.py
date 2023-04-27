from django.contrib.contenttypes.models import ContentType
from like_dislike.models import LikeDislike


def check_like_dislike(user, obj):
    obj_like_check = LikeDislike.objects.filter(
        content_type=ContentType.objects.get_for_model(obj),
        object_id=obj.pk,
        user=user,
    )
    if obj_like_check:
        obj_like_check = obj_like_check.first().vote
    else:
        obj_like_check = None
    return obj_like_check


def check_like_dislike_from_queryset(user, queryset):
    user_ckeck_comments_by_like_dislike = {}

    for query in queryset:
        query_like_check = check_like_dislike(user, query)
        if query_like_check:
            user_ckeck_comments_by_like_dislike[query.id] = query_like_check
    return user_ckeck_comments_by_like_dislike
