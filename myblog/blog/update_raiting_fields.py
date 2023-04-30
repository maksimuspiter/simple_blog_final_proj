from django.contrib.auth.decorators import user_passes_test


def check_admin(user):
    return user.is_superuser


@user_passes_test(check_admin)
def update_raiting_field(request, queryset=None):
    if queryset:
        for item in queryset:
            item.update_raiting()
        return "successfully updated"
    return "function did not get queryset"
