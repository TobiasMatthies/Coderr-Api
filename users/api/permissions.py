from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission: only allow owners to update.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsBusinessUser(BasePermission):
    """
    Custom permission: only allow business users to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'business'


class IsCustomerUser(BasePermission):
    """
    Custom permission: only allow customer users to access certain views.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'
