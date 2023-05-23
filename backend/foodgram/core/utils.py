from core.enums import BynaryFilterValues

ADMIN_GROUP_NAME = 'admins'


def is_in_admin_group(user):
    return user.groups.filter(name=ADMIN_GROUP_NAME).exists()


def is_admin(user):
    return (
        user.is_superuser or user.is_authenticated and is_in_admin_group(user)
    )


def get_filtered_queryset(self, queryset, user_property, value):
    user = self.request.user
    if user.is_anonymous:
        return queryset.none()
    recipe_ids = getattr(user, user_property).values_list(
        'recipe__id', flat=True
    )
    if value == BynaryFilterValues.select.value:
        return queryset.filter(id__in=recipe_ids)
    if value == BynaryFilterValues.exclude.value:
        return queryset.exclude(id__in=recipe_ids)

    raise ValueError(f'{value} is not a valid filter value')
