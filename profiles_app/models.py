from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    file = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, default='')
    tel = models.CharField(max_length=20, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def type(self):
        return self.user.type
    
    @property
    def email(self):
        return self.user.email
    
    @property
    def username(self):
        return self.user.username
