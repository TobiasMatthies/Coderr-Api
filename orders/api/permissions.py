from rest_framework.permissions import BasePermission

class IsBusinessOwner(BasePermission):
    """
    Custom permission: only allow the creator of the offer detail to update.
    """
    def has_object_permission(self, request, view, obj):
        return obj.offerdetail.offer.user == request.user
