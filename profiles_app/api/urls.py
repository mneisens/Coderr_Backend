from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/', views.business_profiles, name='business-profiles'),
    path('profiles/customer/', views.customer_profiles, name='customer-profiles'),
]