
from rest_framework.permissions import BasePermission
# from rest_framework.permissions import IsAdminUser, SAFE_METHODS

# class IsAdmin(I
# sAdminUser):

#     def has_permission(self, request, view):
#         is_admin = super(
#             IsAdmin,
#             self).has_permission(request, view)
#         # Python3: is_admin = super().has_permission(request, view)
#         return request.method in SAFE_METHODS or is_admin

class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)

class IsProjectManager(BasePermission):
    """
    Provides project manager level permission"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_projectmanager)


class IsUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_user)

