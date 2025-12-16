from rest_framework import permissions
from core.apps.accounts.choices.user import PersonTypeChoice


class AdPermission(permissions.BasePermission):

    def __init__(self) -> None:
        ...

    def __call__(self, *args, **kwargs):
        return self

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_authenticated and request.user.person_type == PersonTypeChoice.LEGAL_ENTITY:
            return True
        return False
