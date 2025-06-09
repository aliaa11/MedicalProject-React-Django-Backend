from rest_framework.permissions import BasePermission

class IsRoleAdmin(BasePermission):
    """
    يسمح فقط للمستخدمين اللي عندهم role='admin'
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )
