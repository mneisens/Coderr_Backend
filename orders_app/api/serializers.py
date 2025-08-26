from rest_framework import serializers
from ..models import Order
from offers_app.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    """
    Main serializer for Order objects.
    Used for listing, retrieving, and updating orders.
    """
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 
                 'delivery_time_in_days', 'price', 'features', 'offer_type', 
                 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'customer_user', 'business_user', 'title', 
                           'revisions', 'delivery_time_in_days', 'price', 
                           'features', 'offer_type', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating orders.
    Creates an order from an offer detail.
    """
    offer_detail_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['offer_detail_id']

    def validate_offer_detail_id(self, value):
        """
        Validates that the offer detail exists.
        """
        try:
            offer_detail = OfferDetail.objects.get(id=value)
            return value
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError("Offer detail not found.")

    def create(self, validated_data):
        """
        Creates an order from an offer detail.
        """
        offer_detail_id = validated_data.pop('offer_detail_id')
        offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        
        order = Order.objects.create(
            customer_user=self.context['request'].user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress'
        )
        
        return order
