from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Profile
from .serializers import (
    ProfileSerializer, 
    ProfileUpdateSerializer, 
    ProfileListSerializer,
    CustomerProfileListSerializer
)
from .permissions import IsProfileOwner


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a specific user profile.
    Supports both GET and PATCH operations.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self):
        """
        Returns the profile object for the specified user ID.
        """
        pk = self.kwargs.get('pk')
        return get_object_or_404(Profile, user_id=pk)

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the request method.
        """
        if self.request.method == 'PATCH':
            return ProfileUpdateSerializer
        return ProfileSerializer

    def update(self, request, *args, **kwargs):
        """
        Updates a profile and returns it with 200 status code.
        """
        response = super().update(request, *args, **kwargs)
        
        # Return the full profile data using ProfileSerializer for frontend compatibility
        instance = self.get_object()
        serializer = ProfileSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusinessProfilesView(generics.ListAPIView):
    """
    View for listing all business user profiles.
    Returns a simple list of business profiles without pagination.
    """
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        """
        Returns all business user profiles.
        """
        return Profile.objects.filter(user__type='business').order_by('user__username')

    def list(self, request, *args, **kwargs):
        """
        Lists business profiles and returns them with 200 status code.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfilesView(generics.ListAPIView):
    """
    View for listing all customer user profiles.
    Returns a simple list of customer profiles without pagination.
    """
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        """
        Returns all customer user profiles.
        """
        return Profile.objects.filter(user__type='customer').order_by('user__username')

    def list(self, request, *args, **kwargs):
        """
        Lists customer profiles and returns them with 200 status code.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
