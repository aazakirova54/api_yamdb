from rest_framework import permissions


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or (
                request.user.is_authenticated
                and request.user.is_admin)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    pass


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    pass
