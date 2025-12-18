from rest_framework.permissions import BasePermission
from core.apps.accounts.choices.user import PersonTypeChoice


class EmployeePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
                user.is_authenticated and
                user.person_type == PersonTypeChoice.LEGAL_ENTITY
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
                user.is_authenticated and
                user.person_type == PersonTypeChoice.LEGAL_ENTITY
        )
