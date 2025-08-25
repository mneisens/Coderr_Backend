from django.db import models
from auth_app.models import CustomUser
from offers_app.models import Offer


class Review(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='reviews')
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
        unique_together = ['offer', 'reviewer']
        ordering = ['-updated_at']

    def __str__(self):
        return f"Review von {self.reviewer.username} für {self.offer.title} - {self.rating} Sterne"

    @property
    def business_user(self):
        return self.offer.user
