from rest_framework import permissions
from profiles_app.models import Profile

class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            profile = Profile.objects.get(user=request.user)
            return profile.type == 'customer'
        except Profile.DoesNotExist:
            return False

class IsBusinessUser(permissions.BasePermission):    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            profile = Profile.objects.get(user=request.user)
            return profile.type == 'business'
        except Profile.DoesNotExist:
            return False

class IsOrderParticipant(permissions.BasePermission):    
    def has_object_permission(self, request, view, obj):
        return obj.customer_user == request.user or obj.business_user == request.user
