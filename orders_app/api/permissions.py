from rest_framework import permissions
from profiles_app.models import Profile


class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.type == 'customer'


class IsBusinessUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.type == 'business'


class IsOrderParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer_user == request.user or obj.business_user == request.user
