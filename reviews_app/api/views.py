from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q
from ..models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer, ReviewUpdateSerializer
from .permissions import IsCustomerUser, IsReviewOwner
from rest_framework.exceptions import ValidationError

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']

    def get_queryset(self):
        return Review.objects.all()
    
    def list(self, request, *args, **kwargs):
        if request.user.type == 'business':
            queryset = self.get_queryset().filter(business_user=request.user)
        else:
            queryset = self.get_queryset().filter(reviewer=request.user)
        
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            if ordering == 'updated_at':
                queryset = queryset.order_by('updated_at')
            elif ordering == '-updated_at':
                queryset = queryset.order_by('-updated_at')
            elif ordering == 'rating':
                queryset = queryset.order_by('rating')
            elif ordering == '-rating':
                queryset = queryset.order_by('-rating')
            else:
                queryset = queryset.order_by('-updated_at')
        else:
            queryset = queryset.order_by('-updated_at')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCustomerUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsReviewOwner()]
        return super().get_permissions()

    def perform_create(self, serializer):
        business_user = serializer.validated_data['business_user']
        if Review.objects.filter(reviewer=self.request.user, business_user=business_user).exists():
            raise ValidationError('Sie haben bereits eine Bewertung für diesen Business User abgegeben.')
        serializer.save(reviewer=self.request.user)
