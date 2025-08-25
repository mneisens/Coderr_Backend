from rest_framework import serializers
from ..models import Order
from offers_app.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'customer_user', 'business_user', 'title', 'revisions',
            'delivery_time_in_days', 'price', 'features', 'offer_type',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField(required=False, allow_null=True)

    def validate_offer_detail_id(self, value):
        if value is None:
            raise serializers.ValidationError("This field is required.")
        return value

    def create(self, validated_data):
        offer_detail_id = validated_data.get('offer_detail_id')

        if not offer_detail_id:
            raise serializers.ValidationError({"offer_detail_id": "This field is required."})

        try:
            offer_detail = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                {"offer_detail_id": "Das angegebene Angebotsdetail wurde nicht gefunden."})

        order_data = {
            'customer_user': self.context['request'].user,
            'business_user': offer_detail.offer.user,
            'title': offer_detail.title,
            'revisions': offer_detail.revisions,
            'delivery_time_in_days': offer_detail.delivery_time_in_days,
            'price': offer_detail.price,
            'features': offer_detail.features,
            'offer_type': offer_detail.offer_type,
            'status': 'in_progress'
        }

        return Order.objects.create(**order_data)
