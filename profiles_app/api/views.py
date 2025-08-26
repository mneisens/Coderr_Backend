from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, ProfileListSerializer, CustomerProfileListSerializer
from .permissions import IsProfileOwner
from auth_app.models import CustomUser


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ProfileUpdateSerializer
        return ProfileSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        profile = get_object_or_404(Profile, user__id=pk)
        self.check_object_permissions(self.request, profile)
        return profile

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        if response.status_code == 200:
            profile = self.get_object()
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def business_profiles(request):
    profiles = Profile.objects.filter(user__type='business')
    serializer = ProfileListSerializer(profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_profiles(request):
    profiles = Profile.objects.filter(user__type='customer')
    serializer = CustomerProfileListSerializer(profiles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
