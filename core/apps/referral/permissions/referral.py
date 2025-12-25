from rest_framework import permissions


class ReferralPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.can_create_referral:
            return True
        return False
