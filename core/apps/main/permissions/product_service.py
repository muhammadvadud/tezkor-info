from rest_framework import permissions
from core.apps.accounts.choices.user import PersonTypeChoice


class ProductServicePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "POST":
            return request.user.person_type == PersonTypeChoice.LEGAL_ENTITY

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ["PATCH", "PUT", "DELETE"]:
            return (
                    request.user.person_type == PersonTypeChoice.LEGAL_ENTITY
                    and obj.company == request.user
            )
        return False
