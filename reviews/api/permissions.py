from rest_framework.permissions import BasePermission

class IsReviewOwner(BasePermission):
    """
    Custom permission: only allow owners to update.
    """
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
