from core.apps.accounts.choices.user import RoleChoice
from rest_framework import permissions


class ConfirmationAdsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == RoleChoice.ADMIN:
            return True
        return False
