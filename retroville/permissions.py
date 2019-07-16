from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):

        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin
