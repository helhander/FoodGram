from rest_framework.permissions import BasePermission, SAFE_METHODS

from core.utils import isInAdminGroup


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_superuser
            or user.is_authenticated
            and isInAdminGroup(user)
        )

class IsMeAndSuperUserAndAdmin(BasePermission):
    def has_permission(self, request, view):
        return True
        try:
            username_me = view.kwargs.get('username') == 'me'
        except AttributeError:
            username_me = False

        return request.user.is_authenticated and any(
            (
                username_me,
                request.user.is_superuser,
            )
        )