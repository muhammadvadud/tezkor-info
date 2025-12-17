from rest_framework import permissions
from core.apps.accounts.choices.user import PersonTypeChoice


class ProductServicePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return False
