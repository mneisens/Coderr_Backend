from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/', views.BusinessProfilesView.as_view(), name='business-profiles'),
    path('profiles/customer/', views.CustomerProfilesView.as_view(), name='customer-profiles'),
]
