from django.db import models
from auth_app.models import CustomUser

class Review(models.Model):
    business_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_received',limit_choices_to={'type': 'business'}
    )
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(choices=[
        (1, '1 Stern'),
        (2, '2 Sterne'),
        (3, '3 Sterne'),
        (4, '4 Sterne'),
        (5, '5 Sterne'),
    ])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['business_user', 'reviewer']
        ordering = ['-updated_at']

    def __str__(self):
        return f"Review von {self.reviewer.username} für {self.business_user.username} - {self.rating} Sterne"
