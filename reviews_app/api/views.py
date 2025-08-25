from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Q
from ..models import Review
from .serializers import ReviewSerializer, ReviewUpdateSerializer, ReviewListSerializer, ReviewUpdateOnlySerializer, ReviewCreateOnlySerializer
from .permissions import IsCustomerUser, IsReviewOwner
from rest_framework.exceptions import ValidationError

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['reviewer']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']

    def get_queryset(self):
        return Review.objects.all()
    
    def list(self, request, *args, **kwargs):
        offers_view = request.query_params.get('offers_view', 'false').lower() == 'true'
        offer_id = request.query_params.get('offer', None)
        business_user_id = request.query_params.get('business_user', None)
        
        old_business_user_id = request.query_params.get('business_user_id', None)
        reviewer_id = request.query_params.get('reviewer_id', None)
        
        if request.user.type == 'business':
            queryset = self.get_queryset().filter(offer__user=request.user)
        else:
            if offers_view and offer_id:
                queryset = self.get_queryset().filter(offer=offer_id)
            elif offers_view and business_user_id:
                from offers_app.models import Offer
                offer = Offer.objects.filter(user_id=business_user_id).first()
                if offer:
                    queryset = self.get_queryset().filter(offer=offer.id)
                else:
                    queryset = self.get_queryset().none()
            elif old_business_user_id:
                from offers_app.models import Offer
                offer = Offer.objects.filter(user_id=old_business_user_id).first()
                if offer:
                    queryset = self.get_queryset().filter(offer=offer.id)
                else:
                    queryset = self.get_queryset().none()
            elif reviewer_id:
                queryset = self.get_queryset().filter(reviewer=reviewer_id)
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
        if self.action in ['update', 'partial_update']:
            return ReviewUpdateSerializer
        elif self.action in ['retrieve', 'list']:
            return ReviewListSerializer
        return ReviewListSerializer
    
    def get_serializer(self, *args, **kwargs):
        if self.action in ['update', 'partial_update']:
            return ReviewUpdateOnlySerializer(*args, **kwargs)
        elif self.action == 'create':
            return ReviewCreateOnlySerializer(*args, **kwargs)
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCustomerUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsReviewOwner()]
        return super().get_permissions()
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def perform_create(self, serializer):
        try:
            offer = serializer.validated_data.get('offer')
            if not offer:
                raise ValidationError('Kein Angebot gefunden für diesen Business User.')
            
            if Review.objects.filter(reviewer=self.request.user, offer=offer).exists():
                raise ValidationError('Sie haben bereits eine Bewertung für dieses Angebot abgegeben.')
            
            serializer.save(reviewer=self.request.user)
        except Exception as e:
            raise ValidationError(f'Fehler beim Erstellen der Bewertung: {str(e)}')
    
    def create(self, request, *args, **kwargs):
        offer_id = request.query_params.get('offer_id')
        if offer_id:
            request.data['offer'] = offer_id
        
        return super().create(request, *args, **kwargs)
