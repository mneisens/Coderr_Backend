from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from ..models import Offer, OfferDetail
from .serializers import (
    OfferListSerializer, 
    OfferCreateSerializer, 
    OfferRetrieveSerializer,
    OfferDetailSerializer
)
from .permissions import IsBusinessUser, IsOfferOwner
from .filters import OfferFilter
from profiles_app.models import Profile

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OfferCreateSerializer
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
        return Offer.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer_data = serializer.validated_data
        offer_data['user'] = request.user
        
        offer = serializer.save()
        
        retrieve_serializer = OfferRetrieveSerializer(offer)
        return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)

class OfferDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
