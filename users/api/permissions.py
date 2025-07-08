from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission: only allow owners to update.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
