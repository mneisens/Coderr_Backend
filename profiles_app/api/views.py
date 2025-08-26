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
        return Response(response.data, status=status.HTTP_200_OK)


class BusinessProfilesView(generics.ListAPIView):
    """
    View for listing all business user profiles.
    Returns a paginated list of business profiles.
    """
    serializer_class = ProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns all business user profiles.
        """
        return Profile.objects.filter(user__type='business')

    def list(self, request, *args, **kwargs):
        """
        Lists business profiles and returns them with 200 status code.
        """
        response = super().list(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)


class CustomerProfilesView(generics.ListAPIView):
    """
    View for listing all customer user profiles.
    Returns a paginated list of customer profiles.
    """
    serializer_class = CustomerProfileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns all customer user profiles.
        """
        return Profile.objects.filter(user__type='customer')

    def list(self, request, *args, **kwargs):
        """
        Lists customer profiles and returns them with 200 status code.
        """
        response = super().list(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)
