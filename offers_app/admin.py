from django.contrib import admin
from .models import Offer, OfferDetail

class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 1

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'updated_at', 'min_price', 'min_delivery_time']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description', 'user__username']
    inlines = [OfferDetailInline]
    
    def min_price(self, obj):
        return obj.min_price
    min_price.short_description = 'Minimaler Preis'
    
    def min_delivery_time(self, obj):
        return obj.min_delivery_time
    min_delivery_time.short_description = 'Minimale Lieferzeit'

@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = ['title', 'offer', 'price', 'delivery_time_in_days', 'offer_type']
    list_filter = ['offer_type', 'delivery_time_in_days']
    search_fields = ['title', 'offer__title']
