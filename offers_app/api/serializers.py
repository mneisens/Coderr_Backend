from rest_framework import serializers
from ..models import Offer, OfferDetail
from profiles_app.models import Profile

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username']

class OfferListSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()
    user_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 
                 'details', 'min_price', 'min_delivery_time', 'user_details']
    
    def get_details(self, obj):
        details = obj.details.all()
        return [{'id': detail.id, 'url': f'/api/offerdetails/{detail.id}/'} for detail in details]
    
    def get_user_details(self, obj):
        try:
            profile = Profile.objects.get(user=obj.user)
            return UserDetailsSerializer(profile).data
        except Profile.DoesNotExist:
            return None

class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailCreateSerializer(many=True)
    
    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']
    
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        
        return offer
    
    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Ein Angebot muss genau 3 Details enthalten.")
        return value

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class OfferRetrieveSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()
    
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 
                 'details', 'min_price', 'min_delivery_time']
    
    def get_details(self, obj):
        details = obj.details.all()
        return [{'id': detail.id, 'url': f'http://127.0.0.1:8000/api/offerdetails/{detail.id}/'} for detail in details]
