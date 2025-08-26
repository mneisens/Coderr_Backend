from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Min
from ..models import Offer, OfferDetail
from .serializers import (
    OfferListSerializer,
    OfferCreateSerializer,
    OfferRetrieveSerializer,
    OfferDetailSerializer,
    OfferUpdateSerializer,
    OfferDetailUpdateSerializer
)
from .permissions import IsBusinessUser, IsOfferOwner
from .filters import OfferFilter
from profiles_app.models import Profile


class OfferPagination(PageNumberPagination):
    """
    Custom pagination class for Offer endpoints.
    Allows clients to specify page size via 'page_size' query parameter.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 6


class OfferViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Offer objects.
    Provides CRUD operations for offers with filtering, searching, and ordering capabilities.
    """
    queryset = Offer.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at']
    pagination_class = OfferPagination

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action.
        Different serializers are used for different operations to optimize performance.
        """
        if self.action == 'create':
            return OfferCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OfferUpdateSerializer
        elif self.action == 'retrieve':
            return OfferRetrieveSerializer
        else:
            return OfferListSerializer

    def get_permissions(self):
        """
        Returns the appropriate permission classes based on the action.
        Ensures proper access control for different operations.
        """
        if self.action in ['create']:
            return [IsAuthenticated(), IsBusinessUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOfferOwner()]
        elif self.action in ['retrieve']:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        """
        Returns the queryset for offers with optional ordering.
        Supports ordering by minimum price and creation date.
        """
        queryset = Offer.objects.all()
        ordering = self.request.query_params.get('ordering', None)
        
        if ordering == 'min_price':
            queryset = queryset.prefetch_related('details').order_by('details__price')
        elif ordering == '-min_price':
            queryset = queryset.prefetch_related('details').order_by('-details__price')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def perform_create(self, serializer):
        """
        Performs the actual creation of an offer.
        Automatically sets the current user as the offer creator.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Creates a new offer and returns it with 201 status code.
        Overrides default create method to ensure proper status code.
        """
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Updates an existing offer and returns it with 200 status code.
        Overrides default update method to ensure proper status code.
        """
        response = super().update(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates an existing offer and returns it with 200 status code.
        Overrides default partial_update method to ensure proper status code.
        """
        response = super().partial_update(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes an offer and returns 204 status code (no content).
        Overrides default destroy method to ensure proper status code.
        """
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferDetailViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing OfferDetail objects.
    Provides CRUD operations for offer details (individual service packages within offers).
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action.
        """
        if self.action in ['update', 'partial_update']:
            return OfferDetailUpdateSerializer
        return OfferDetailSerializer

    def get_permissions(self):
        """
        Returns the appropriate permission classes based on the action.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOfferOwner()]
        return [IsAuthenticated()]
