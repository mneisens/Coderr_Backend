from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ..models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from .permissions import IsCustomerUser, IsOrderParticipant
from auth_app.models import CustomUser

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderParticipant]
    pagination_class = None  # Deaktiviert Paginierung für einfaches Array
    
    def get_queryset(self):
        return Order.objects.filter(
            Q(customer_user=self.request.user) | Q(business_user=self.request.user)
        ).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCustomerUser()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_count(request, business_user_id):
    """Gibt die Anzahl der laufenden Bestellungen eines Business Users zurück"""
    try:
        business_user = get_object_or_404(CustomUser, id=business_user_id, type='business')
        count = Order.objects.filter(
            business_user=business_user,
            status='in_progress'
        ).count()
        
        return Response({'order_count': count})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def completed_order_count(request, business_user_id):
    """Gibt die Anzahl der abgeschlossenen Bestellungen eines Business Users zurück"""
    try:
        business_user = get_object_or_404(CustomUser, id=business_user_id, type='business')
        count = Order.objects.filter(
            business_user=business_user,
            status='completed'
        ).count()
        
        return Response({'completed_order_count': count})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
