from django.db import models
from django.conf import settings

class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='offer_images/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def min_price(self):
        """Gibt den niedrigsten Preis aller Details zurück"""
        details = self.details.all()
        if details.exists():
            return float(min(detail.price for detail in details))
        return 0.0
    
    @property
    def min_delivery_time(self):
        """Gibt die kürzeste Lieferzeit aller Details zurück"""
        details = self.details.all()
        if details.exists():
            return int(min(detail.delivery_time_in_days for detail in details))
        return 0

class OfferDetail(models.Model):
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=200)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.offer.title} - {self.title}"
