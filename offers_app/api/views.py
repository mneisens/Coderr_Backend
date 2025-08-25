from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return OfferCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OfferUpdateSerializer
        elif self.action == 'retrieve':
            return OfferRetrieveSerializer
        else:
            return OfferListSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [IsAuthenticated(), IsBusinessUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOfferOwner()]
        elif self.action in ['retrieve']:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
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
        serializer.save(user=self.request.user)


class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return OfferDetailUpdateSerializer
        return OfferDetailSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOfferOwner()]
        return [IsAuthenticated()]
