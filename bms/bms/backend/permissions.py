from rest_framework import permissions

SAFE_METHODS = ['GET']

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if (request.user and request.user.is_authenticated()):
            return request.method in SAFE_METHODS or request.user.is_staff
        return False
