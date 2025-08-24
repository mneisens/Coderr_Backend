from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, order_count, completed_order_count

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('order-count/<int:business_user_id>/', order_count, name='order-count'),
    path('completed-order-count/<int:business_user_id>/', completed_order_count, name='completed-order-count'),
]
