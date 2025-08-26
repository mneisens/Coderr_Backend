from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from ..models import Review
from .serializers import ReviewSerializer, ReviewUpdateOnlySerializer, ReviewCreateOnlySerializer
from .permissions import IsCustomerUser, IsReviewOwner
from rest_framework.exceptions import ValidationError
from offers_app.models import Offer


class ReviewPagination(PageNumberPagination):
    """
    Custom pagination class for Review endpoints.
    Allows clients to specify page size via 'page_size' query parameter.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 6


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Review objects.
    Provides CRUD operations for reviews with filtering and ordering capabilities.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['reviewer']
    ordering_fields = ['updated_at', 'rating']
    ordering = ['-updated_at']
    pagination_class = ReviewPagination

    def get_queryset(self):
        """
        Returns the base queryset for reviews.
        """
        return Review.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Lists reviews with advanced filtering and pagination.
        Supports filtering by business user, offer, and reviewer.
        """
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
                offer = Offer.objects.filter(user_id=business_user_id).first()
                if offer:
                    queryset = self.get_queryset().filter(offer=offer.id)
                else:
                    queryset = self.get_queryset().none()
            elif old_business_user_id:
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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action.
        """
        if self.action == 'create':
            return ReviewCreateOnlySerializer
        elif self.action in ['update', 'partial_update']:
            return ReviewUpdateOnlySerializer
        elif self.action in ['retrieve', 'list']:
            return ReviewSerializer
        return ReviewSerializer

    def get_permissions(self):
        """
        Returns the appropriate permission classes based on the action.
        """
        if self.action == 'create':
            return [IsAuthenticated(), IsCustomerUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsReviewOwner()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        """
        Updates a review and returns the full review object.
        Handles 404 and permission errors with appropriate status codes.
        """
        try:
            response = super().update(request, *args, **kwargs)

            instance = self.get_object()
            serializer = ReviewSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Http404:
            return Response({'error': 'No Review matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes a review.
        Handles 404 and permission errors with appropriate status codes.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Http404:
            return Response({'error': 'No Review matches the given query.'}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """
        Performs the actual creation of a review.
        Validates that the user hasn't already reviewed this offer.
        """
        print(f"=== PERFORM CREATE ===")
        print(f"Validated data: {serializer.validated_data}")
        
        offer = serializer.validated_data.get('offer')
        if not offer:
            print("ERROR: Kein Angebot gefunden")
            raise ValidationError('Kein Angebot gefunden für diesen Business User.')

        print(f"Angebot gefunden: {offer.id}")

        if Review.objects.filter(reviewer=self.request.user, offer=offer).exists():
            print("ERROR: Bewertung existiert bereits")
            raise ValidationError('Sie haben bereits eine Bewertung für dieses Angebot abgegeben.')

        print("Speichere Bewertung...")
        serializer.save(reviewer=self.request.user)
        print("Bewertung erfolgreich gespeichert")
        print(f"=== END PERFORM CREATE ===")

    def create(self, request, *args, **kwargs):
        """
        Creates a new review with business user to offer mapping.
        Handles duplicate review validation and returns appropriate error messages.
        """
        print(f"=== CREATE REVIEW ===")
        print(f"Request data: {request.data}")
        print(f"Query params: {request.query_params}")
        print(f"User: {request.user}")
        
        data = request.data.copy()
        
        if 'business_user' in data and not data.get('offer'):
            business_user_id = data['business_user']
            try:
                offer = Offer.objects.filter(user_id=business_user_id).first()
                if offer:
                    data['offer'] = offer.id
                    print(f"Angebot gefunden für Business User {business_user_id}: {offer.id}")
                else:
                    return Response(
                        {'error': 'Kein Angebot für diesen Business User gefunden.'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                return Response(
                    {'error': f'Fehler beim Finden des Angebots: {str(e)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            
            offer = serializer.validated_data.get('offer')
            if offer and Review.objects.filter(reviewer=request.user, offer=offer).exists():
                return Response(
                    {'error': 'Sie haben bereits eine Bewertung für dieses Angebot abgegeben.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            review = serializer.save(reviewer=request.user)
            
            response_serializer = ReviewSerializer(review)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"ERROR in create: {str(e)}")
            if "UNIQUE constraint failed" in str(e):
                return Response(
                    {'error': 'Sie haben bereits eine Bewertung für dieses Angebot abgegeben.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response({'error': f'Fehler beim Erstellen der Bewertung: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
