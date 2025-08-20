from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    
    email = models.EmailField(unique=True)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'type']
    
    def __str__(self):
        return self.username



