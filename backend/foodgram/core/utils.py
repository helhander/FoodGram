ADMIN_GROUP_NAME = 'admins'


def is_in_admin_group(user):
    return user.groups.filter(name=ADMIN_GROUP_NAME).exists()


def is_admin(user):
    return (
        user.is_superuser or user.is_authenticated and is_in_admin_group(user)
    )
