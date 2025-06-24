from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    TYPE_CHOICES = [('customer', 'customer'),
                   ('bussiness', 'bussines'),
        ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, choices=TYPE_CHOICES)
    firstname = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, default="")
    file = models.ImageField(upload_to='media', blank=True)
    location = models.CharField(max_length=30, blank=True)
    tel = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)






