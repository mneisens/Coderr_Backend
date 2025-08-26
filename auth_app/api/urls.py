from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.register, name='registration'),
    path('login/', views.login, name='login'),
]
