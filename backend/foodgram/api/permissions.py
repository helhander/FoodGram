from core.utils import is_admin
from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return is_admin(user)


class ReadOnlyOrAuthorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            request.method in SAFE_METHODS
            or obj.author == user
            or is_admin(user)
        )


class RetrieveOrMeActions(BasePermission):
    def has_permission(self, request, view):
        if (
            view.action == 'retrieve'
            or view.action == 'me'
            and request.user.is_authenticated
        ):
            return True
        return False
