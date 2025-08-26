from rest_framework import serializers
from ..models import Review
from offers_app.models import Offer


class ReviewSerializer(serializers.ModelSerializer):
    """
    Main serializer for Review objects.
    Used for listing and retrieving reviews.
    """
    business_user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def get_business_user(self, obj):
        """
        Returns the business user ID from the associated offer.
        """
        return obj.offer.user.id


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'description']


class ReviewListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing reviews.
    Used specifically for review list endpoints.
    """
    business_user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'rating', 'description', 'created_at', 'updated_at', 'business_user']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def get_business_user(self, obj):
        """
        Returns the business user ID from the associated offer.
        """
        return obj.offer.user.id


class ReviewUpdateOnlySerializer(serializers.ModelSerializer):
    """
    Serializer for updating reviews.
    Only allows updating rating and description.
    """
    class Meta:
        model = Review
        fields = ['rating', 'description']


class ReviewCreateOnlySerializer(serializers.ModelSerializer):
    """
    Serializer for creating reviews.
    Handles business_user to offer mapping.
    """
    business_user = serializers.IntegerField(required=False)
    business_user_id = serializers.IntegerField(required=False)

    class Meta:
        model = Review
        fields = ['offer', 'rating', 'description', 'business_user', 'business_user_id']

    def validate(self, data):
        """
        Validates review data and handles business user to offer mapping.
        """
        business_user_id = data.get('business_user') or data.get('business_user_id')
        
        if not data.get('offer') and business_user_id:
            offer = Offer.objects.filter(user_id=business_user_id).first()
            if offer:
                data['offer'] = offer
            else:
                raise serializers.ValidationError("No offer found for this business user.")
        
        data.pop('business_user', None)
        data.pop('business_user_id', None)
        
        return data
