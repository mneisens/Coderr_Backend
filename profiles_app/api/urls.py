from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('business/', views.business_profiles, name='business-profiles'),
    path('customer/', views.customer_profiles, name='customer-profiles'),
]