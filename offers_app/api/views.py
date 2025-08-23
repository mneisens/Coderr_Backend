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
from profiles_app.models import Profile

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['creator_id']
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
        queryset = Offer.objects.all()
        
        creator_id = self.request.query_params.get('creator_id', None)
        if creator_id is not None:
            queryset = queryset.filter(user_id=creator_id)
        
        min_price = self.request.query_params.get('min_price', None)
        if min_price is not None:
            queryset = queryset.filter(details__price__gte=min_price).distinct()

        max_delivery_time = self.request.query_params.get('max_delivery_time', None)
        if max_delivery_time is not None:
            queryset = queryset.filter(details__delivery_time_in_days__lte=max_delivery_time).distinct()
        
        return queryset
    
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
