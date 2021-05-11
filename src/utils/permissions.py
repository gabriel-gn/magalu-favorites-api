from rest_framework import permissions


class SuperuserPermission(permissions.BasePermission):
    """
    Apenas pode acessar a view caso seja superuser.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser
