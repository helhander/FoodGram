from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


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